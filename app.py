import streamlit as st

from modules import Analysis

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
author_readability_df = analysis.author_readability(known_words_size, 10, 250)
st.dataframe(author_readability_df)
