from collections import namedtuple
from string import punctuation

import pandas as pd


with open("../assets/diederich.txt") as f:
    diederich_vocab_raw = [l.split(";")[0] for l in f.readlines()[3:]]
diederich_vocab = []
for v in diederich_vocab_raw:
    if " " in v:
        v = v.split(" ")[0]
    v = v.strip(punctuation)
    diederich_vocab.append(v)


LexiconOptions = namedtuple("LexiconOptions", "type n")
    
    
class Lexicon:
    def __init__(self, freq_table_path: str, options: LexiconOptions):
        freq_table = pd.read_csv(freq_table_path, index_col=0)
        freq_table = freq_table.sort_values(by=["count"], ascending=False)
        if options.type == "freq":
            self.lexicon = freq_table[:options.n]
        elif options.type == "perc":
            n = int(len(freq_table) * options.n)
            self.lexicon = freq_table[:n]
        else:
            raise AssertionError(f"{options.type} is not a valid lexicon type")
