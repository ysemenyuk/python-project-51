import pytest
from os import listdir
from os.path import join, isdir
import requests
from urllib.parse import urlparse
import requests_mock
from page_loader.page_loader import download
from page_loader.utils import make_file_name, read_file

session = requests.Session()
adapter = requests_mock.Adapter()
session.mount('mock://', adapter)


PAGE_URL = 'http://mega-loader.test.com'

PAGE_NAME = 'mega-loader-test-com.html'
FILES_DIR_NAME = 'mega-loader-test-com_files'
CSS_FILE_NAME = 'mega-loader-test-com-files-style.css'
HTML_FILE_NAME = 'mega-loader-test-com-courses.html'
IMG_FILE_NAME = 'mega-loader-test-com-files-image.png'
JS_FILE_NAME = 'mega-loader-test-com-files-script.js'

CSS_FILE_URL = f'{PAGE_URL}/files/style.css'
HTML_FILE_URL = f'{PAGE_URL}/courses'
IMG_FILE_URL = f'{PAGE_URL}/files/image.png'
JS_FILE_URL = f'{PAGE_URL}/files/script.js'

FIXTURES_DIR = 'tests/fixtures'
FILES_COUNT = 4

page_path = join(FIXTURES_DIR, 'source_page.html')
css_file_path = join(FIXTURES_DIR, 'files/style.css')
html_file_path = join(FIXTURES_DIR, 'courses.html')
img_file_path = join(FIXTURES_DIR, 'files/image.png')
js_file_path = join(FIXTURES_DIR, 'files/script.js')

expected_html_path = join(FIXTURES_DIR, 'expected_html.html')

data = [
    (CSS_FILE_URL, CSS_FILE_NAME),
    (HTML_FILE_URL, HTML_FILE_NAME),
    (IMG_FILE_URL, IMG_FILE_NAME),
    (JS_FILE_URL, JS_FILE_NAME)
    ]


@pytest.mark.parametrize('link, file_name', data)
def test_make_file_name(link, file_name):
    assert make_file_name(urlparse(link)) == file_name


def test_page_loader(tmpdir, requests_mock):
    requests_mock.get(PAGE_URL, text=read_file(page_path))
    requests_mock.get(CSS_FILE_URL, text=read_file(css_file_path))
    requests_mock.get(HTML_FILE_URL, text=read_file(html_file_path))
    requests_mock.get(IMG_FILE_URL, content=read_file(img_file_path,
                                                      type='rb'))
    requests_mock.get(JS_FILE_URL, text=read_file(js_file_path))

    # html

    output_file_path = download(PAGE_URL, tmpdir)
    expected_file_path = join(tmpdir, PAGE_NAME)

    assert output_file_path == expected_file_path

    output_html = read_file(output_file_path)
    expected_html = read_file(expected_html_path)

    assert output_html == expected_html

    # files

    files_dir = join(tmpdir, FILES_DIR_NAME)

    assert isdir(files_dir)
    assert len(listdir(files_dir)) == FILES_COUNT

    output_css = read_file(join(files_dir, CSS_FILE_NAME))
    expected_css = read_file(css_file_path)

    assert output_css == expected_css

    output_html = read_file(join(files_dir, HTML_FILE_NAME))
    expected_html = read_file(html_file_path)

    assert output_html == expected_html

    output_image = read_file(join(files_dir, IMG_FILE_NAME), type='rb')
    expected_image = read_file(img_file_path, type='rb')

    assert output_image == expected_image

    output_js = read_file(join(files_dir, JS_FILE_NAME))
    expected_js = read_file(js_file_path)

    assert output_js == expected_js
