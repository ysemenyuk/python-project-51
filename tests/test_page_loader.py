import pytest
import os
import requests
from requests.exceptions import RequestException
import requests_mock
from page_loader.page_loader import download


session = requests.Session()
adapter = requests_mock.Adapter()
session.mount('mock://', adapter)


def read(file_path):
    with open(file_path, 'r') as f:
        result = f.read()
    return result

src_file = os.path.join('tests/fixtures', 'page.html')
exp_file = os.path.join('tests/fixtures', 'expected.html')
test_url = 'http://test.com'


def test_page_loader(tmpdir, requests_mock):
    data = read(src_file)
    requests_mock.get(test_url, text=data)
    output_file_path = download(test_url, tmpdir)

    actual = read(output_file_path)
    expected = read(exp_file)

    assert actual == expected


def test_exception(tmpdir, requests_mock):
    with pytest.raises(ValueError):
        data = read(src_file)
        requests_mock.get(test_url, text=data)
        non_existent_dir = os.path.join(tmpdir, 'abc')
        download(test_url, non_existent_dir)

    with pytest.raises(RequestException):
        data = read(src_file)
        requests_mock.get(test_url, status_code=404)
        download(test_url, tmpdir)
