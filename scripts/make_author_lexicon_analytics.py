"""
Create table of percent of words known and percent of known lemmata
for some specifed n.
"""
import os

import pandas as pd

from modules import Lexicon, LexiconOptions


METHOD = "freq"
n = 2000


if __name__ == "__main__":
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
    lexicon_opts = LexiconOptions("freq", 2000)
    full_corpus_lexicon = Lexicon(
        "../frequency_tables/full_corpus_no_ner.csv",
        lexicon_opts
    )
    full_corpus_lemmata = full_corpus_lexicon.lexicon.index.tolist()
    author_lexicons = {}
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
    author_lexicons_df = pd.DataFrame.from_dict(
        author_lexicons, orient="index", columns=["perc_known_unique_lemmata", "perc_known_words"]
    )
    author_lexicons_df.to_csv("../analytics/author_lexicon.csv")
