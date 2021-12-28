# Need to set path env var before importing cltk
import os
from pathlib import Path
data_path = os.getcwd() + "/data"
Path(data_path).mkdir(parents=True, exist_ok=True)
os.environ["CLTK_DATA"] = data_path

import streamlit as st

from modules import Analysis, download_data, Lexicon, LexiconOptions


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

# Frequency table
st.header("Frequency Tables")
st.write("Create table of most frequent words in Classical Latin.")
freq_table_size = st.number_input(
    "Set size of most frequent words",
    help="Set the number of most frequent words known for analysis",
    min_value=1,
    value=2000,
    key=1
)
lexicon_opts = LexiconOptions("freq", freq_table_size)
full_corpus_lexicon = Lexicon("frequency_tables/full_corpus_no_ner.csv", lexicon_opts)
freq_table = full_corpus_lexicon.to_freq_table()
st.dataframe(freq_table)
st.download_button(
    label="Download Frequency Table",
    data=convert_dataframe(freq_table),
    file_name=f"frequency_table_{freq_table_size}.csv",
    mime="text/csv"
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
    key=1
)
author_readability_df = analysis.author_readability(known_words_size)
st.dataframe(author_readability_df)
st.download_button(
    label="Download Author Readability Data",
    data=convert_dataframe(author_readability_df),
    file_name=f"author_readability_stats_{known_words_size}.csv",
    mime="text/csv"
)

# Author readability sampling
st.header("Author Readability Sampling Statistics")
st.write(
    """
    Create tables of statistics for authors to compute their readability according to multiple metrics by sampling *n* number of pages.\n
    Use the first input box below to change the size of known words, i.e., the set of *n* most frequent words in Classical Latin.\n
    The second two input boxes set the parameters for sampling the text. \n
    The first two columns in the table below are the mean and standard deviation of the percent of unique words in an 
    author that a reader would recognize assuming they know all of the words in the known words list. 
    The second two columns are the mean and standard deviation of the percent of total words a reader would recognizer.\n
    **NOTE: This analysis can take a long time to run on a large number of samples.**
    """
)
known_words_size_sampling = st.number_input(
    "Set size of known words",
    help="Set the number of most frequent words known for analysis",
    min_value=1,
    value=2000,
    key=2
)
n_samples = st.number_input(
    "Number of samples per author",
    help="Set the number of samples to be taken for each author",
    min_value=1,
    value=1,
)
sample_size = st.number_input(
    "Sample size in words",
    help="Set how many words is included in each sample",
    min_value=1,
    value=250
)
author_readability_sampling_df = analysis.author_readability_sampling(known_words_size, n_samples, sample_size)
st.dataframe(author_readability_sampling_df)
st.download_button(
    label="Download Author Readability Sampling Data",
    data=convert_dataframe(author_readability_sampling_df),
    file_name=f"author_readability_sampling_stats_{known_words_size}_{n_samples}_{sample_size}.csv",
    mime="text/csv"
)
