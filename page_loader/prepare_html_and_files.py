from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from page_loader.utils import make_file_name


DEFAULT_PARSER = 'html.parser'
ASSETS_DICT = {
    'img': 'src',
    'link': 'href',
    'script': 'src',
}


def prepare_html_and_files(page, page_url, files_dir_name):
    local_assets = []
    soup = BeautifulSoup(page, DEFAULT_PARSER)
    elements = soup.find_all(ASSETS_DICT)

    for element in elements:
        attr_name = ASSETS_DICT.get(element.name)
        element_url = element.attrs.get(attr_name)

        if not element_url:
            continue

        file_url = urlparse(urljoin(page_url.geturl(), element_url))

        if file_url.netloc != page_url.netloc:
            continue

        file_name = make_file_name(file_url)
        element[attr_name] = f'{files_dir_name}/{file_name}'
        local_assets.append((file_name, file_url.geturl()))

    return soup.prettify(), local_assets
