# Need to set path env var before importing cltk
import os
import json
from pathlib import Path

data_path = os.getcwd() + "/data"
Path(data_path).mkdir(parents=True, exist_ok=True)
os.environ["CLTK_DATA"] = data_path

import streamlit as st
import pandas as pd
from cltk.data.fetch import FetchCorpus

from modules import Analysis, Lexicon, LexiconOptions, AUTHOR_DIRS, AUTHOR_TXTS, CORPUS_NAME


@st.cache
def download_data():
    """
    Download data and create json of texts.
    """
    if Path("data/lat").exists():
        print("Data already downloaded")
        return
    # Download Latin Library
    corpus_downloader = FetchCorpus(language="lat")
    corpus_downloader.import_corpus("lat_text_latin_library")
    corpus_downloader.import_corpus("lat_models_cltk")
    # Create corpus json
    texts_path = os.getcwd() + "/data/lat/text/lat_text_latin_library/"
    corpora = {}
    for a in AUTHOR_DIRS:
        author_dir = texts_path + a
        texts = [
            author_dir + "/" + t for t in os.listdir(author_dir) if t[-3:] == "txt"
        ]
        corpora[a] = texts
    for k, v in AUTHOR_TXTS.items():
        texts = [texts_path + t for t in v]
        corpora[k] = texts
    with open(f"assets/{CORPUS_NAME}_corpora.json", "w") as f:
        json.dump(corpora, f, indent=4, sort_keys=True)
    print("Downloaded data")
download_data()

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

# Frequency table
st.header("Frequency Tables")
st.write("Create table of most frequent words in Classical Latin.")
authors = [a[:-11] for a in os.listdir("frequency_tables") if a[-11:] == "_no_ner.csv"]
authors.sort()
author = st.selectbox("Select author or full corpus for lexicon", authors)
freq_table_size = st.number_input(
    "Set size of most frequent words",
    help="Set the number of most frequent words known for analysis",
    min_value=1,
    value=2000,
    key=1,
)
lexicon_opts = LexiconOptions("freq", freq_table_size)
lexicon = Lexicon(f"frequency_tables/{author}_no_ner.csv", lexicon_opts)
freq_table = lexicon.to_freq_table()
st.dataframe(freq_table)
st.download_button(
    label="Download Frequency Table",
    data=convert_dataframe(freq_table),
    file_name=f"frequency_table_{freq_table_size}.csv",
    mime="text/csv",
)

# Author readability
st.header("Author Readability Statistics")
st.write(
    """
    Create tables of statistics for authors to compute their readability according to multiple metrics.\n
    Use the input box below to change the size of known words, i.e., the set of *n* most frequent words in Classical Latin.\n
    The first column in the table below is the percent of unique words in an author that a reader would recognize assuming
    they know all of the words in the known words list. The second column is the percent of total words a reader would recognizer.
    """
)
known_words_size = st.number_input(
    "Set size of known words",
    help="Set the number of most frequent words known for analysis",
    min_value=1,
    value=2000,
    key=1,
)
author_readability_df = analysis.author_readability(known_words_size)
st.dataframe(author_readability_df)
st.download_button(
    label="Download Author Readability Data",
    data=convert_dataframe(author_readability_df),
    file_name=f"author_readability_stats_{known_words_size}.csv",
    mime="text/csv",
)

# Author readability sampling
st.header("Author Readability Sampling Statistics")
st.write(
    """
    Create tables of statistics for authors to compute their readability according to multiple metrics by sampling *n* number of pages.\n
    Use the select box below to choose the size of the known lexicon.\n
    The first two columns in the table below are the mean and standard deviation of the percent of unique words in an 
    author that a reader would recognize assuming they know all of the words in the known words list. 
    The second two columns are the mean and standard deviation of the percent of total words a reader would recognizer.\n
    """
)
known_words_size_sampling = st.selectbox(
    "Set size of known words",
    [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000],
    index=3,
)
author_readability_sampling_df = pd.read_csv(
    f"analytics/author_lexicon_n_{known_words_size_sampling}.csv", index_col=0
)
author_readability_sampling_df.sort_index(inplace=True)
author_readability_sampling_df.drop("cato", inplace=True)
author_readability_sampling_df.drop(
    columns=["perc_known_unique_lemmata", "perc_known_words"], axis=1, inplace=True
)
st.dataframe(author_readability_sampling_df)
st.download_button(
    label="Download Author Readability Sampling Data",
    data=convert_dataframe(author_readability_sampling_df),
    file_name=f"author_readability_sampling_stats_{known_words_size}.csv",
    mime="text/csv",
)
