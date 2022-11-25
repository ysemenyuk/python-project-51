import argparse


DESCRIPTION = 'download page'
HELP = 'set output dir'
URL = 'page_url'


def get_parser():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(URL, type=str)
    parser.add_argument('--output', '-o', type=str, default='', help=HELP)
    return parser
