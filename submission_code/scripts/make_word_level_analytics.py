"""
Generate word level analytics.
"""
import os

import numpy as np
import pandas as pd

if __name__ == "__main__":
    full_corpus_df = pd.read_csv(
        "../frequency_tables/full_corpus_no_ner.csv", index_col=0
    )
    # Compute global frequency
    total_words_corpus = full_corpus_df["count"].sum()
    full_corpus_df["global_frequency"] = np.log(
        total_words_corpus / full_corpus_df["count"]
    )
    # Compute local frequency
    freq_table_paths = [
        "../frequency_tables/" + p
        for p in os.listdir("../frequency_tables")
        if p != "full_corpus_no_ner.csv"
    ]
    local_freq = {}
    for p in freq_table_paths:
        df = pd.read_csv(p, index_col=0)
        total_words_author = df["count"].sum()
        for i, r in df.iterrows():
            if i not in local_freq:
                local_freq[i] = (total_words_author / r["count"]) * (
                    total_words_corpus / total_words_author
                )
            else:
                local_freq[i] += (total_words_author / r["count"]) * (
                    total_words_corpus / total_words_author
                )
    local_freq_df = pd.DataFrame.from_dict(
        local_freq, orient="index", columns=["local_frequency"]
    )
    local_freq_df["local_frequency"] = np.log(local_freq_df["local_frequency"])
    analytics_df = pd.merge(
        full_corpus_df, local_freq_df, left_index=True, right_index=True
    )
    analytics_df["rareness"] = (
        analytics_df["global_frequency"] * analytics_df["local_frequency"]
    )
    analytics_df.to_csv("../analytics/word_level_rareness.csv")
