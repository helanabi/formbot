#!/usr/bin/env python

import argparse
import csv
import sys
import time
from playwright.sync_api import sync_playwright, TimeoutError

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="CSV data file")
    parser.add_argument("url", help="Web page URL")
    parser.add_argument("--action", "-a", default="submit",
                        help="Action button name (default: submit)")
    parser.add_argument("--pause", "-p", action="store_true",
                        help="Run headed browser and pause at the end")
    parser.add_argument("--delay", "-d", default=0, type=int,
                        help="Add delay between submissions in seconds "
                        "(default: 0)")
    parser.add_argument("--timeout", "-t", default=30, type=float,
                        help="Time to wait for elements in seconds. "
                        "Pass 0 to disable timeout (default: 30)")
    return parser.parse_args()

def warn(name, value):
    print(f"Warning: Unexpected value for '{name}': {value}. Skipping...",
          file=sys.stderr)

def enter_value(page, field, value):
    control = page.get_by_label(field).or_(
        page.get_by_placeholder(field)).first

    if control.get_attribute("type") == "checkbox":
        if value == "yes":
            control.check()
        elif value == "no":
            control.uncheck()
        else:
            warn(field, value)
    elif control.evaluate("e => e.tagName") == "SELECT":
        try:
            control.select_option(value)
        except TimeoutError:
            warn(field, value)
    else:
        control.fill(value)

def main(args):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.pause)
        page = browser.new_page()
        page.set_default_timeout(args.timeout * 1000)
        page.goto(args.url)

        with open(args.csv, newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                for field, value in zip(header, row):
                    enter_value(page, field, value)
                page.get_by_role("button", name=args.action).click()
                time.sleep(args.delay)

        if args.pause:
            page.pause()

        browser.close()

if __name__ == "__main__":
    try:
        main(parse_args())
    except TimeoutError as e:
        print(e, file=sys.stderr)
