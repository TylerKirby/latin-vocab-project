import json
import os

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

    def author_readability(self, lexicon_size) -> pd.DataFrame:
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
            # Stats
            author_readability[author] = [
                perc_known_lemmata,
                perc_known_words,
            ]
        author_readability_df = pd.DataFrame.from_dict(
            author_readability,
            orient="index",
            columns=[
                "perc_known_unique_lemmata",
                "perc_known_words",
            ],
        )
        return author_readability_df
