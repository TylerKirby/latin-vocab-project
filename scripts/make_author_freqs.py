"""
Iterate through JSON of authors and text paths, and process them into CSVs of frequency tables.
"""

import argparse
import json
import os

import pandas as pd
from tqdm import tqdm

from modules import CorpusAnalytics

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--ner", help="Include analysis of NER", default=False)
    parser.add_argument(
        "-c",
        "--corpora_path",
        help="Path to JSON of texts for corpora",
        default="../assets/classical_corpora.json",
    )
    parser.add_argument(
        "-a",
        "--all",
        help="If true then script will analyse all texts, otherwise it will only analyze texts without an analyse ",
        default=1,
        type=int,
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        help="directory to save analyses",
        default="../frequency_tables",
    )
    args = parser.parse_args()

    OUTPUT_DIR = args.output_dir

    with open(args.corpora_path) as f:
        corpora = json.load(f)

    analytics = CorpusAnalytics("lat", lemmatizer_type="lamonpy")

    completed_analyses = [p[:-11] for p in os.listdir(OUTPUT_DIR) if p[-3:] == "csv"]
    with pd.ExcelWriter("../workbooks/vocabulary_freq_no_proper_nouns.xlsx") as writer:
        for author in tqdm(corpora.keys(), desc="Authors"):
            if author in completed_analyses and args.all == 0:
                print(f"Skipping {author}")
                continue
            print(f"Processing {author}")
            vocab_freq = analytics.process_corpus(corpora[author])
            df = pd.DataFrame.from_dict(vocab_freq, orient="index", columns=["count"])
            df.to_csv(f"{OUTPUT_DIR}/{author}_no_ner.csv")
            df.to_excel(writer, sheet_name=author)

    if args.ner:
        with pd.ExcelWriter(
            "../workbooks/vocabulary_freq_with_proper_nouns.xlsx"
        ) as writer:
            for author in tqdm(corpora.keys()):
                vocab_freq = analytics.process_corpus(corpora[author], filter_ner=False)
                df = pd.DataFrame.from_dict(
                    vocab_freq, orient="index", columns=["count"]
                )
                df.to_csv(f"{OUTPUT_DIR}/{author}_ner.csv")
                df.to_excel(writer, sheet_name=author)
