import pandas as pd

from utils.corpus import CorpusAnalytics


if __name__ == "__main__":
    cat_luc_corpus = [
        "/Users/tyler/cltk_data/latin/text/latin_text_latin_library/lucretius/lucretius1.txt",
        "/Users/tyler/cltk_data/latin/text/latin_text_latin_library/lucretius/lucretius2.txt",
        "/Users/tyler/cltk_data/latin/text/latin_text_latin_library/lucretius/lucretius3.txt",
        "/Users/tyler/cltk_data/latin/text/latin_text_latin_library/lucretius/lucretius4.txt",
        "/Users/tyler/cltk_data/latin/text/latin_text_latin_library/lucretius/lucretius5.txt",
        "/Users/tyler/cltk_data/latin/text/latin_text_latin_library/lucretius/lucretius6.txt",
        "/Users/tyler/cltk_data/latin/text/latin_text_latin_library/catullus.txt"
    ]
    analytics = CorpusAnalytics("lat")
    lexicon_freq = analytics.process_corpus(cat_luc_corpus)
    df = pd.DataFrame.from_dict(lexicon_freq, orient="index", columns=["count"])
    df.to_excel("luc_cat_sample.xlsx")
