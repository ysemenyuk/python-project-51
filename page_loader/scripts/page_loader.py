#!/usr/bin/env python3

from page_loader.page_loader import download
from page_loader.cli import cli


def main():
    args = cli()
    print('page_url:', args.page_url, 'output:', args.output)

    file_path = download(args.page_url, args.output)

    print(file_path)


if __name__ == '__main__':
    main()
