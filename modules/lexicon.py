from string import punctuation

with open("../assets/diederich.txt") as f:
    diederich_vocab_raw = [l.split(";")[0] for l in f.readlines()[3:]]
diederich_vocab = []
for v in diederich_vocab_raw:
    if " " in v:
        v = v.split(" ")[0]
    v = v.strip(punctuation)
    diederich_vocab.append(v)
