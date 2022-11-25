# from page_loader.logger import logging
from progress.bar import Bar
import requests
from os.path import join


DOWNLOADING = 'Downloading files:'


def download_files(files, dir):
    bar = Bar(DOWNLOADING, max=len(files))
    exeptions = []
    for name, url in files:
        try:
            res = requests.get(url)
            res.raise_for_status()
        except Exception as e:
            exeptions.append(e)
            continue

        file_path = join(dir, name)
        with open(file_path, 'wb') as f:
            f.write(res.content)
        bar.next()

    bar.finish()

    return exeptions
