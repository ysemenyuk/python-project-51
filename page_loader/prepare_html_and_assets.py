from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from page_loader.utils import make_file_name

assets_map = {
    'img': 'src',
    'link': 'href',
    'script': 'src',
}


def prepare_html_and_assets(page, page_url, files_dir_name):
    local_assets = []
    soup = BeautifulSoup(page, 'html.parser')
    elements = soup.find_all(assets_map)

    for el in elements:
        attr_name = assets_map.get(el.name)
        el_url = el.attrs.get(attr_name)
        
        if not el_url:
            continue
        
        file_url = urlparse(urljoin(page_url.geturl(), el_url))

        if file_url.netloc != page_url.netloc:
            continue
        
        file_name = make_file_name(file_url)
        el[attr_name] = f'{files_dir_name}/{file_name}'
        local_assets.append((file_name, file_url.geturl()))

    return soup.prettify(), local_assets
