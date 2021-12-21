"""
Create table of percent of words known and percent of known lemmata
for some specifed n.
"""
import argparse
import json
import os
import random

import numpy as np
import pandas as pd

from modules import CorpusAnalytics, Lexicon, LexiconOptions

random.seed(1)


# Lexicon parameters
METHOD = "freq"

# Page sampled parameters
SAMPLES = 10
SAMPLE_SIZE = 250


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--n_lexical_size", required=True, type=int, help="size of lexicon"
    )
    args = parser.parse_args()

    n = args.n_lexical_size

    print(f"Computing lexical statistics with n={n}")

    frequency_table_path = "../frequency_tables"
    author_table_paths = [
        frequency_table_path + "/" + p
        for p in os.listdir(frequency_table_path)
        if p[-3:] == "csv" and "full_corpus" not in p
    ]
    output_path = "../analytics"
    author_stats = {}
    full_corpus_df = pd.read_csv(
        "../frequency_tables/full_corpus_no_ner.csv", index_col=0
    )
    lexicon_opts = LexiconOptions("freq", n)
    full_corpus_lexicon = Lexicon(
        "../frequency_tables/full_corpus_no_ner.csv", lexicon_opts
    )
    full_corpus_lemmata = full_corpus_lexicon.lexicon.index.tolist()
    author_lexicons = {}
    with open("../assets/classical_corpora.json") as f:
        texts_json = json.load(f)
    frequenter = CorpusAnalytics("lat", lemmatizer_type="lamonpy")
    for p in author_table_paths:
        author = p.split("/")[-1][:-11]
        df = pd.read_csv(p, index_col=0)
        author_lemmata = df.index.tolist()
        same_lemmata = list(set(full_corpus_lemmata) & set(author_lemmata))
        # Percent of known unique lemmata
        perc_known_lemmata = len(same_lemmata) / len(author_lemmata)
        # Percent of total know words
        total_words = df["count"].sum()
        known_words = df.loc[same_lemmata]["count"].sum()
        perc_known_words = known_words / total_words
        author_lexicons[author] = [perc_known_lemmata, perc_known_words]
        # Percent of words known from sampled pages
        author_texts = texts_json[author]
        page_known_lemmata = []
        page_known_words = []
        for i in range(SAMPLES):
            random_text = random.choice(author_texts)
            try:
                with open(random_text) as f:
                    text = f.read()
            except FileNotFoundError:
                print(f"Text {random_text} not found")
                continue
            tokenized = text.split(" ")
            if len(tokenized) <= 250:
                print(f"Sample too small for {random_text}")
                continue
            possible_page_start = len(tokenized) - SAMPLE_SIZE
            page_start = random.randint(0, possible_page_start)
            page_end = page_start + SAMPLE_SIZE
            page = " ".join(tokenized[page_start:page_end])
            page_freq = frequenter.process_text(page)
            page_lemmata = list(page_freq.lemmata_frequencies.keys())
            page_same_lemmata = list(set(full_corpus_lemmata) & set(page_lemmata))
            perc_known_lemmata = len(page_same_lemmata) / len(author_lemmata)
            page_known_lemmata.append(perc_known_lemmata)
            page_df = pd.DataFrame.from_dict(
                page_freq.lemmata_frequencies, orient="index", columns=["count"]
            )
            page_total_words = page_df["count"].sum()
            if page_total_words == 0:
                print(
                    f"Page total words is 0 for {random_text} with page start {page_start}"
                )
                continue
            page_known_words_count = page_df.loc[page_same_lemmata]["count"].sum()
            page_perc_known_words = page_known_words_count / page_total_words
            page_known_words.append(page_perc_known_words)
        page_known_lemmata = np.array(page_known_lemmata)
        page_known_words = np.array(page_known_words)

        # Stats
        author_lexicons[author] = [
            perc_known_lemmata,
            perc_known_words,
            page_known_lemmata.mean(),
            page_known_lemmata.std(),
            page_known_words.mean(),
            page_known_words.std(),
        ]
    author_lexicons_df = pd.DataFrame.from_dict(
        author_lexicons,
        orient="index",
        columns=[
            "perc_known_unique_lemmata",
            "perc_known_words",
            "page_known_lemmata_mean",
            "page_known_lemmata_std",
            "page_known_words_mean",
            "page_known_words_std",
        ],
    )
    author_lexicons_df.to_csv(f"../analytics/author_lexicon_n_{n}.csv")
