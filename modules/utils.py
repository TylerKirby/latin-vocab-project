import json
import os

from cltk.data.fetch import FetchCorpus

from .corpus_constants import AUTHOR_DIRS, AUTHOR_TXTS, CORPUS_NAME


def download_data():
    """
    Download data and create json of texts.
    """
    # Download Latin Library
    corpus_downloader = FetchCorpus(language="lat")
    corpus_downloader.import_corpus("lat_text_latin_library")
    corpus_downloader.import_corpus("lat_models_cltk")
    # Create corpus json
    texts_path = os.getcwd() + "/data/lat/text/lat_text_latin_library/"
    corpora = {}
    for a in AUTHOR_DIRS:
        author_dir = texts_path + a
        texts = [
            author_dir + "/" + t for t in os.listdir(author_dir) if t[-3:] == "txt"
        ]
        corpora[a] = texts
    for k, v in AUTHOR_TXTS.items():
        texts = [texts_path + t for t in v]
        corpora[k] = texts
    with open(f"assets/{CORPUS_NAME}_corpora.json", "w") as f:
        json.dump(corpora, f, indent=4, sort_keys=True)
