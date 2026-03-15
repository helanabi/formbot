## Overview

**Formbot** uses [Playwright](https://playwright.dev) to automate filling web
forms from CSV data.

## Features

- Automatic waits for operations with a configurable timeout
- Dynamic action element resolution with a configurable text
- Runs headless or headed with the option to pause once done
- User defined delay
- Handles irregular data and missing values gracefully

## Requirements

- Python 3.9+
- Chromium
- Runtime dependencies:

Archlinux      | Debian (and derivatives, e.g. Ubuntu)
-----------------------------------------------------
`icu`          | `libicu74`
`libxml2`      | `libxml2`
`libxslt`      | `libxslt1.1`
`flite`        | `libflite1`
`harfbuzz-icu` | `libharfbuzz-icu0`
`libmanette`   | `libmanette-0.2-0`
`enchant`      | `libenchant-2-2`
`hyphen`       | `libhyphen0`
`woff2`        | `libwoff1`

## Usage

```
usage: formbot [-h] [--action ACTION] [--pause] [--delay DELAY]
               [--timeout TIMEOUT]
               csv url

positional arguments:
  csv                   CSV data file
  url                   Web page URL

options:
  -h, --help            show this help message and exit
  --action, -a ACTION   Action button name (default: submit)
  --pause, -p           Run headed browser and pause at the end
  --delay, -d DELAY     Add delay between submissions in seconds (default: 0)
  --timeout, -t TIMEOUT
                        Time to wait for elements in seconds. Pass 0 to
                        disable timeout (default: 30)
```
## LICENSE

This project is licensed under the MIT License.
