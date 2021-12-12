import json
import os
import random

import numpy as np
import pandas as pd

from .corpus import CorpusAnalytics
from .lexicon import Lexicon, LexiconOptions


class Analysis:
    def __init__(self, corpus_json_path, freq_tables_path, full_corpus_freq_table_path):
        with open(corpus_json_path) as f:
            self.corpus_json = json.load(f)
        self.author_table_paths = [
            freq_tables_path + "/" + p
            for p in os.listdir(freq_tables_path)
            if p[-3:] == "csv" and "full_corpus" not in p
        ]
        self.full_corpus_freq_table_path = full_corpus_freq_table_path
        self.frequenter = CorpusAnalytics("lat", lemmatizer_type="lamonpy")

    def author_readability(self, lexicon_size, n_samples, sample_size) -> pd.DataFrame:
        lexicon_opts = LexiconOptions("freq", lexicon_size)
        full_corpus_lexicon = Lexicon(self.full_corpus_freq_table_path, lexicon_opts)
        full_corpus_lemmata = full_corpus_lexicon.lexicon.index.tolist()
        author_readability = {}
        for p in self.author_table_paths:
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
            author_readability[author] = [perc_known_lemmata, perc_known_words]
            # Percent of words known from sampled pages
            author_texts = self.corpus_json[author]
            page_known_lemmata = []
            page_known_words = []
            for i in range(n_samples):
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
                possible_page_start = len(tokenized) - sample_size
                page_start = random.randint(0, possible_page_start)
                page_end = page_start + sample_size
                page = " ".join(tokenized[page_start:page_end])
                page_freq = self.frequenter.process_text(page)
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
            author_readability[author] = [
                perc_known_lemmata,
                perc_known_words,
                page_known_lemmata.mean(),
                page_known_lemmata.std(),
                page_known_words.mean(),
                page_known_words.std(),
            ]
        author_readability_df = pd.DataFrame.from_dict(
            author_readability,
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
        return author_readability_df
