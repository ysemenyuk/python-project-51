from page_loader.logger import logging
from progress.bar import Bar
import requests
from os.path import join

def download_assets(files, dir):
    bar = Bar('Download_files:', max=len(files))
    exeptions = []
    for name, url in files:
        try:
            res = requests.get(url)
            res.raise_for_status()
        except Exception as e:
            # logging.info("file not found: %s" % url)
            exeptions.append(e)
            continue

        file_path = join(dir, name)
        with open(file_path, 'wb') as f:
            f.write(res.content)
        bar.next()

    bar.finish()
    
    if len(exeptions):
        logging.info(f"{len(exeptions)} files did't download")
        for e in exeptions:
            logging.error(e)
    