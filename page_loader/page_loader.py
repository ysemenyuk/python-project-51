import requests
from urllib.parse import urlparse, urlunparse
import re
import os
from bs4 import BeautifulSoup


def format_name(name):
    words = re.split('[^а-яa-z0-9]', name)
    return "-".join(list(filter(None, words)))


def make_name(url, type):
    main_name = format_name(f'{url.netloc}/{url.path}')
    return f'{main_name}{type}'


def make_file_name(url):
    u = urlparse(url)
    fileName, fileExtension = os.path.splitext(u.path)
    name = format_name(f'{u.netloc}/{fileName}')
    # print('fileName', fileName, 'fileExtension:', fileExtension)
    if fileExtension:
        return f'{name}{fileExtension}'
    return f'{name}.html'


assets_map = {
    'img': 'src',
    'link': 'href',
    'script': 'src',
}


def download(input_url, input_path):
    page_url = urlparse(input_url)

    html_file_name = make_name(page_url, '.html')
    files_dir_name = make_name(page_url, '_files')

    full_path_to_page = os.path.join(os.getcwd(), input_path)

    html_file_path = os.path.join(full_path_to_page, html_file_name)
    files_dir_path = os.path.join(full_path_to_page, files_dir_name)

    res = requests.get(input_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    local_assets = []

    for tag_name, attr_name in assets_map.items():
        elements = soup.find_all(tag_name)
        filtered = list(filter(lambda el: el.attrs.get(attr_name), elements))
        for el in filtered:
            scheme, netloc, *rest = urlparse(el.attrs.get(attr_name))
            if not netloc:
                scheme = page_url.scheme
                netloc = page_url.netloc
            if netloc == page_url.netloc:
                file_url = urlunparse((scheme, netloc, *rest))
                file_name = make_file_name(file_url)
                el[attr_name] = f'{files_dir_name}/{file_name}'
                local_assets.append((file_name, file_url))

    with open(html_file_path, 'w') as f:
        f.write(soup.prettify())

    os.mkdir(files_dir_path)
    
    def download_files(files, dir):
        for name, url in files:
            r = requests.get(url)
            file_path = os.path.join(dir, name)

            with open(file_path, 'wb') as f:
                f.write(r.content)
    
    download_files(local_assets, files_dir_path)       

    # for name, url in local_assets:
    #     r = requests.get(url)
    #     file_path = os.path.join(files_dir_path, name)

    #     with open(file_path, 'wb') as f:
    #         f.write(r.content)

    return html_file_name
