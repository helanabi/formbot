#!/usr/bin/env python

import argparse
import csv
import sys
import time
from playwright.sync_api import expect, sync_playwright, TimeoutError

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="CSV data file")
    parser.add_argument("url", help="Web page URL")
    parser.add_argument("--action", "-a", default="submit",
                        help="Action button name (default: submit)")
    parser.add_argument("--pause", "-p", action="store_true",
                        help="Run headed browser and pause at the end")
    parser.add_argument("--delay", "-d", default=0, type=float,
                        help="Add delay between submissions in seconds "
                        "(default: 0)")
    parser.add_argument("--timeout", "-t", default=30, type=float,
                        help="Time to wait for elements in seconds. "
                        "Pass 0 to disable timeout (default: 30)")
    return parser.parse_args()

def warn(name, value):
    print(f"Warning: Unexpected value for '{name}': {value}. Skipping...",
          file=sys.stderr)

def get_control(page, field):
    """Find a form control and its type in a page.

    Return a tuple of control type and its locator.
    """
    control = page.get_by_label(field).or_(
        page.get_by_placeholder(field)).first

    tag = control.evaluate("e => e.tagName").lower()

    if tag == "input":
        return control.get_attribute("type"), control
    else:
        return tag, control

def enter_value(page, field, value, default):
    type_, ctrl = get_control(page, field)

    if type_ == "checkbox":
        true_values = ("yes", "y", "true", "1")
        false_values = ("no", "n", "false", "0")

        if value not in true_values + false_values:
            warn(field, value or "*empty*")
            value = default

        if value in true_values:
            ctrl.check()
        else:
            ctrl.uncheck()

    elif type_ == "select":
        try:
            ctrl.select_option(value)
        except TimeoutError:
            warn(field, value)
            ctrl.select_option(default)
    else:
        ctrl.fill(value)

def resolve_action_ctrl(page, text):
    def is_visible(locator):
        try:
            locator.wait_for()
        except TimeoutError:
            return False
        return True

    for control in (page.get_by_role("button", name=text),
                    page.get_by_role("link", name=text),
                    page.get_by_text(text)):
        if is_visible(control):
            return control

def main(args, page):
    page.set_default_timeout(args.timeout * 1000)
    page.goto(args.url)
    
    with open(args.csv, newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        defaults = []

        for field in header:
            type_, ctrl = get_control(page, field)
            if type_ == "checkbox":
                defaults.append("yes" if ctrl.is_checked() else "no")
            else:
                defaults.append(ctrl.input_value())

        for i, row in enumerate(reader):
            for field, value, default in zip(header, row, defaults):
                enter_value(page, field, value, default)
            if not i:
                action_control = resolve_action_ctrl(page, args.action)
                if not action_control:
                    print(f"Error: Action control '{args.action}' not found",
                          file=sys.stderr)
                    sys.exit(1)
            action_control.click()
            page.wait_for_timeout(args.delay * 1000)
            page.wait_for_load_state("networkidle")
            try:
                expect(action_control).to_be_enabled()
            except AssertionError:
                page.goto(args.url)

    if args.pause:
        page.pause()

if __name__ == "__main__":
    with sync_playwright() as p:
        args = parse_args()
        try:
            browser = p.chromium.launch(headless=not args.pause)
            main(args, browser.new_page())
        except TimeoutError as e:
            print(e, file=sys.stderr)
        finally:
            browser.close()
