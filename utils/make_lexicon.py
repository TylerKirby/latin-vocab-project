import argparse
import json

import pandas as pd
from tqdm import tqdm

from utils.corpus import CorpusAnalytics

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--ner", help="Include analysis of NER", default=False)
    parser.add_argument("-c", "--corpora_path", help="Path to JSON of texts for corpora", default="corpora.json")
    args = parser.parse_args()

    with open("corpora.json") as f:
        corpora = json.load(f)
    analytics = CorpusAnalytics("lat", lemmatizer_type="lamonpy")
    with pd.ExcelWriter("../frequency_tables/vocabulary_freq_no_proper_nouns.xlsx") as writer:
        for author in tqdm(corpora.keys(), desc="Authors"):
            print(f"Processing {author}")
            vocab_freq = analytics.process_corpus(corpora[author])
            df = pd.DataFrame.from_dict(vocab_freq, orient="index", columns=["count"])
            df.to_csv(f"../frequency_tables/{author}_no_ner.csv")
            df.to_excel(writer, sheet_name=author)
    if args.ner:
        with pd.ExcelWriter("vocabulary_freq_with_proper_nouns.xlsx") as writer:
            for author in tqdm(corpora.keys()):
                vocab_freq = analytics.process_corpus(corpora[author], filter_ner=False)
                df = pd.DataFrame.from_dict(vocab_freq, orient="index", columns=["count"])
                df.to_excel(writer, sheet_name=author)
