import pytest
import os
import requests
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
    res_file = download(test_url, tmpdir)
    
    actual = read(res_file)
    expected = read(exp_file)
    
    assert actual == expected