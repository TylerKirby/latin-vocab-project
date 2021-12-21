# Need to set path env var before importing cltk
import os
from pathlib import Path
data_path = os.getcwd() + "/data"
Path(data_path).mkdir(parents=True, exist_ok=True)
os.environ["CLTK_DATA"] = data_path

import pandas as pd
import streamlit as st

from modules import Analysis, download_data


download_data()

analysis = Analysis(
    "assets/classical_corpora.json",
    "frequency_tables/",
    "frequency_tables/full_corpus_no_ner.csv",
)

# App header
st.title("Latin Vocabulary Data Explorer")

# Author readability
st.header("Author Readability Statistics")
st.write(
    "Create tables of statistics for authors to compute their readability according to multiple metrics.",
    "Note that statistics for lexical sizes 500 to 5000 in increments of 500 have been precomputed."
)
known_words_size = st.number_input(
    "Set size of known words",
    help="Set the number of most frequent words known for analysis",
    min_value=1,
    value=2000,
)
precomputed_author_readability_n = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
if known_words_size in precomputed_author_readability_n:
    author_readability_df = pd.read_csv(f"analytics/author_lexicon_n_{known_words_size}.csv", index_col=0)
else:
    author_readability_df = analysis.author_readability(known_words_size, 10, 250)
st.dataframe(author_readability_df)
