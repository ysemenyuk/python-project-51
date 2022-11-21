import argparse


DESCRIPTION = 'download page'
HELP = 'set output dir'
URL = 'page_url'


def cli():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(URL, type=str)
    parser.add_argument('--output', type=str, default='', help=HELP)
    return parser.parse_args()
