"""
Compute
"""
import os

import pandas as pd

AUTHOR_LEXICA_PATH = "../frequency_tables"


if __name__ == "__main__":
    lexica_paths = [
        AUTHOR_LEXICA_PATH + "/" + p
        for p in os.listdir(AUTHOR_LEXICA_PATH)
        if p[-3:] == "csv" and "full_corpus" not in p
    ]
    combined_lexica = {}
    for p in lexica_paths:
        df = pd.read_csv(p, names=["lemma", "count"], header=0)
        for r in df.itertuples():
            if r[1] not in combined_lexica:
                combined_lexica[r[1]] = r[2]
            else:
                combined_lexica[r[1]] += r[2]
    combined_lexica = dict(
        sorted(combined_lexica.items(), key=lambda item: item[1], reverse=True)
    )
    final_df = pd.DataFrame.from_dict(
        combined_lexica, orient="index", columns=["count"]
    )
    final_df.to_csv(AUTHOR_LEXICA_PATH + "/" + "full_corpus.csv")
    with pd.ExcelWriter("../workbooks/full_corpus.xlsx") as writer:
        final_df.to_excel(writer, sheet_name="full_corpus")
