# Need to set path env var before importing cltk
import os
from pathlib import Path
data_path = os.getcwd() + "/data"
Path(data_path).mkdir(parents=True, exist_ok=True)
os.environ["CLTK_DATA"] = data_path

import streamlit as st

from modules import Analysis, download_data


if len(os.listdir(data_path)) == 0:
    download_data()
else:
    print("Data already downloaded")


@st.cache
def convert_dataframe(df):
    """
    Convert dataframe to binary form for downloading.
    """
    return df.to_csv().encode("utf-8")


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
    "Create tables of statistics for authors to compute their readability according to multiple metrics."
)
known_words_size = st.number_input(
    "Set size of known words",
    help="Set the number of most frequent words known for analysis",
    min_value=1,
    value=2000,
)
author_readability_df = analysis.author_readability(known_words_size)
st.dataframe(author_readability_df)
st.download_button(
    label="Download Author Readability Data",
    data=convert_dataframe(author_readability_df),
    file_name=f"author_readability_stats_{known_words_size}.csv",
    mime="text/csv"
)
