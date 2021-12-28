from collections import namedtuple
from string import punctuation

import pandas as pd

LexiconOptions = namedtuple("LexiconOptions", "type n")


class Lexicon:
    def __init__(self, freq_table_path: str, options: LexiconOptions):
        freq_table = pd.read_csv(freq_table_path, index_col=0)
        freq_table = freq_table.sort_values(by=["count"], ascending=False)
        if options.type == "freq":
            self.lexicon = freq_table[: options.n]
        elif options.type == "perc":
            n = int(len(freq_table) * options.n)
            self.lexicon = freq_table[:n]
        else:
            raise AssertionError(f"{options.type} is not a valid lexicon type")

    def to_freq_table(self):
        return self.lexicon
