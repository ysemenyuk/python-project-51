#!/usr/bin/env python3

from page_loader.page_loader import download
from page_loader.cli import get_parser
from requests.exceptions import RequestException
import sys


PAGE_SAVED = 'Page saved successfully: "{}"'


def main():
    parser = get_parser()
    args = parser.parse_args()

    try:
        file_path = download(args.page_url, args.output)
        print(PAGE_SAVED.format(file_path))
    except RequestException as e:
        print(e)
        sys.exit(1)
    except ValueError as e:
        print(e)
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
