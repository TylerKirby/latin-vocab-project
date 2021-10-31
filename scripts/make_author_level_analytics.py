import os

import pandas as pd

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
    word_analytics_df = pd.read_csv("../analytics/word_level_rareness.csv", index_col=0)
    for p in author_table_paths:
        author = p.split("/")[-1][:-11]
        df = pd.read_csv(p, index_col=0)
        # TTR = total unique lemma / total tokens
        total_unique_lemmata = df.shape[0]
        total_words = df["count"].sum()
        TTR = total_unique_lemmata / total_words
        # Hapax richness = total hapax lemmata / total unique lemmata
        total_hapax_lemmata = df.loc[df["count"] == 1].shape[0]
        HR = total_hapax_lemmata / total_unique_lemmata
        # Word rareness = total word rareness
        df = pd.merge(
            df,
            word_analytics_df.drop("count", axis=1),
            left_index=True,
            right_index=True,
        )
        df["rareness"] = df["rareness"] * df["count"]
        R = df["rareness"].sum() / total_words

        author_stats[author] = [TTR, HR, R]
    author_level_analytics_df = pd.DataFrame.from_dict(
        author_stats, orient="index", columns=["TTR", "HR", "R"]
    )
    author_level_analytics_df["R_scaled"] = (
        author_level_analytics_df["R"] - author_level_analytics_df["R"].min()
    ) / (author_level_analytics_df["R"].max() - author_level_analytics_df["R"].min())
    author_level_analytics_df.to_csv("../analytics/author_level_analytics.csv")
