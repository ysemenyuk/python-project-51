import requests
from urllib.parse import urlparse
import re
import os


def download(input_url, input_path):
    path_to_file = os.path.join(os.getcwd(), input_path)
    print(path_to_file)

    url = urlparse(input_url)
    words = re.split('[^а-яa-z0-9]', f'{url.netloc}/{url.path}')
    file_name = f'{"-".join(list(filter(None, words)))}.html'
    print(file_name)

    full_path = os.path.join(path_to_file, file_name)

    r = requests.get(input_url)
    with open(full_path, 'w') as f:
        f.write(r.text)

    return full_path
