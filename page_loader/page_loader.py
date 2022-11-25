import requests
from requests.exceptions import RequestException
from urllib.parse import urlparse
import os
from os.path import join, isdir
from page_loader.logger import logging
from page_loader.download_files import download_files
from page_loader.utils import make_name, make_files_dir, save_html
from page_loader.prepare_html_and_files import prepare_html_and_files


HTML = '.html'
FILES = '_files'
INPUT_PATH_NOT_FOUND = 'Input path "{}" is not found.'
START_DOWNLOAD = 'Start download "{}" in "{}"'
REQUEST = 'Request at "{}"'
REQUEST_ERROR = 'Request errror: {}'
RESPONSE = 'Response status code {}'
PREPARE_DATA = 'Prepare html and links for local assets'
HTML_FILE_CREATED = 'html_file created successfully "{}"'
FILES_DIR_CREATED = 'files_dir created successfully: "{}"'
START_DOWNLOAD_FILES = 'Start download local files. Total count: "{}"'
FINISH_DOWNLOAD_FILES = 'Files download successfully: "{}"'
ERRORS_DOWNLOAD = '"{}" files did not download'
FINISH_DOWNLOAD = 'Finish download "{}"'


def download(input_url, input_path):
    page_url = urlparse(input_url)
    full_path_to_page = join(os.getcwd(), input_path)

    if not isdir(input_path):
        logging.error(INPUT_PATH_NOT_FOUND.format(input_path))
        raise ValueError(INPUT_PATH_NOT_FOUND.format(input_path))

    html_file_name = make_name(page_url, HTML)
    files_dir_name = make_name(page_url, FILES)

    html_file_path = join(full_path_to_page, html_file_name)
    files_dir_path = join(full_path_to_page, files_dir_name)

    logging.info(START_DOWNLOAD.format(input_url, input_path))
    logging.info(REQUEST.format(input_url))

    try:
        res = requests.get(input_url)
        logging.debug(RESPONSE.format(res.status_code))
        res.raise_for_status()
    except RequestException as e:
        logging.error(REQUEST_ERROR.format(e))
        raise RequestException(e) from e

    logging.info(PREPARE_DATA.format())

    html, files = prepare_html_and_files(res.text, page_url, files_dir_name)

    if len(files):
        make_files_dir(files_dir_path)
        logging.info(FILES_DIR_CREATED.format(files_dir_name))

        logging.info(START_DOWNLOAD_FILES.format(len(files)))
        errors = download_files(files, files_dir_path)

        if len(errors):
            for err in errors:
                logging.warning(err)

        logging.info(FINISH_DOWNLOAD_FILES.format(len(files) - len(errors)))

    save_html(html, html_file_path)
    logging.info(HTML_FILE_CREATED.format(html_file_name))
    logging.info(FINISH_DOWNLOAD.format(html_file_path))

    return html_file_name
