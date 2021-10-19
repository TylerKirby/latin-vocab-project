"""
Script for combining all csvs into a single excel file.
"""
import argparse
import os

import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_dir",
        type=str,
        help="directory of files to combine",
        default="../frequency_tables",
    )
    parser.add_argument(
        "-o",
        "--output_path",
        type=str,
        help="path to save csv",
        default="../frequency_tables/classical_corpus_no_ner.xlsx",
    )
    args = parser.parse_args()

    INPUT_DIR = args.input_dir
    OUTPUT_PATH = args.output_path

    files_to_combine = [
        INPUT_DIR + "/" + p for p in os.listdir(INPUT_DIR) if p[-3:] == "csv"
    ]
    with pd.ExcelWriter(OUTPUT_PATH) as writer:
        for f in files_to_combine:
            df = pd.read_csv(f, index_col=False)
            title = f.split("/")[-1][:-4]
            df.to_excel(writer, sheet_name=title)
