Latin Vocabulary Project
=
Repository for code and data related to Latin vocabulary project.

# Running the App

Run the app with `streamlit run app.py`.

# Project Structure

## `analytics`
Data sets computed from frequency tables are stored here.

## `assets`
Anacillary files such as corpora configurations are stored here.

## `frequency_tables`
This folder contains computed frequency tables by author.

## `modules`
This files define the framework used for the project.

## `notebooks`
All Jupyter notebooks are stored here.
- `author_level_stats`: Exploratory data analysis of author level stats.
- `genre_analysis`: Exploratory data analysis of how genre relates to lexical difficulty.
- `ner_experiment`: Notebook showing results of corpus module on a sample text.
- `word_level_metrics_experiment`: Exploratory data analysis of word level stats.

## `samples`
Files generated for tests or other samples.

## `scripts`
Scripts for generating data and analyses.
- `make_author_freqs`: Create frequency tables for authors.
- `make_author_level_analytics`: Create author level analytics table.
- `make_corpus_list`: Create corpus JSON for `make_author_freqs` script.
- `make_freq_workbook`: Create excel file from all frequency table.
- `make_full_corpus`: Create frequency table that covers the whole corpus.
- `make_work_level_analytics`: Create data set for word level stats.
