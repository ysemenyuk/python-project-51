import re
import os
import shutil
from os.path import splitext, isdir


def format_name(name):
    words = re.split('[^а-яa-z0-9]', name)
    return "-".join(list(filter(None, words)))


def make_name(url, type):
    main_name = format_name(f'{url.netloc}/{url.path}')
    return f'{main_name}{type}'


def make_file_name(url):
    fileName, fileExtension = splitext(url.path)
    name = format_name(f'{url.netloc}/{fileName}')
    if fileExtension:
        return f'{name}{fileExtension}'
    return f'{name}.html'


def make_files_dir(files_dir_path):
    if isdir(files_dir_path):
        shutil.rmtree(files_dir_path)

    os.mkdir(files_dir_path)


def save_html(html, html_file_path):
    with open(html_file_path, 'w') as f:
        f.write(html)
