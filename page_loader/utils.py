import re
from os.path import splitext

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
