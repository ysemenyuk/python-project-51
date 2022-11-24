#!/usr/bin/env python3

from page_loader.page_loader import download
from page_loader.cli import get_parser
from page_loader.logger import logging
from requests.exceptions import HTTPError
import sys


def main():
    parser = get_parser()
    args = parser.parse_args()
    # print('page_url:', args.page_url, 'output:', args.output)
    
    try:
        file_path = download(args.page_url, args.output)
        print(f'Page saved in {file_path}')
    except HTTPError:
        logging.error('HTTPError')
        sys.exit(1)
    except PermissionError:
        logging.error('PermissionError')
        sys.exit(1)
    except FileNotFoundError:
        logging.error('FileNotFoundError')
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
