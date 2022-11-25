import pytest
from os.path import join
import requests
from requests.exceptions import RequestException
import requests_mock
from page_loader.page_loader import download
from page_loader.utils import read_file


session = requests.Session()
adapter = requests_mock.Adapter()
session.mount('mock://', adapter)


PAGE_URL = 'http://mega-loader.test.com'
FIXTURES_DIR = 'tests/fixtures'

page_path = join(FIXTURES_DIR, 'source_page.html')
expected_html_path = join(FIXTURES_DIR, 'expected_html.html')


def test_exception(tmpdir, requests_mock):
    with pytest.raises(ValueError):
        requests_mock.get(PAGE_URL, text=read_file(page_path))
        non_existent_dir = join(tmpdir, 'abc')

        download(PAGE_URL, non_existent_dir)

    with pytest.raises(RequestException):
        requests_mock.get(PAGE_URL, status_code=404)

        download(PAGE_URL, tmpdir)
