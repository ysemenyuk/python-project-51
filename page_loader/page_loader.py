import requests
from urllib.parse import urlparse, urljoin
import os
import shutil
from page_loader.logger import logging
from page_loader.download_assets import download_assets
from page_loader.utils import make_name
from page_loader.prepare_html_and_assets import prepare_html_and_assets


def download(input_url, input_path):
    page_url = urlparse(input_url)
    full_path_to_page = os.path.join(os.getcwd(), input_path)

    if not os.path.isdir(full_path_to_page):
        raise FileNotFoundError

    html_file_name = make_name(page_url, '.html')
    files_dir_name = make_name(page_url, '_files')
    
    html_file_path = os.path.join(full_path_to_page, html_file_name)
    files_dir_path = os.path.join(full_path_to_page, files_dir_name)

    try:
        res = requests.get(input_url)
        res.raise_for_status()
    except:
        raise

    html, assets = prepare_html_and_assets(res.text, page_url, files_dir_name)

    with open(html_file_path, 'w') as f:
        f.write(html)
    
    logging.info("html_file created successfully: %s in %s" % (html_file_name, input_path))
        
    if os.path.isdir(files_dir_path):
        shutil.rmtree(files_dir_path)

    os.mkdir(files_dir_path)

    logging.info("files_dir created successfully: %s" % files_dir_name)

    download_assets(assets, files_dir_path)

    return html_file_name
