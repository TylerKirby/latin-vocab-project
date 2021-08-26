import json
import pandas as pd

from utils.corpus import CorpusAnalytics


if __name__ == "__main__":
    with open("corpora.json") as f:
        corpora = json.load(f)
    analytics = CorpusAnalytics("lat")
    with pd.ExcelWriter("vocabulary_freq.xlsx") as writer:
        for author in corpora.keys():
            vocab_freq = analytics.process_corpus(corpora[author])
            df = pd.DataFrame.from_dict(vocab_freq, orient="index", columns=["count"])
            df.to_excel(writer, sheet_name=author)
