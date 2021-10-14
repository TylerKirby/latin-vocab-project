import json
import os

CORPUS_NAME = "classical"
AUTHOR_DIRS = [
    "vergil",
    "caesar",
    "cicero",
    "horace",
    "ovid",
    "lucan",
    "juvenal",
    "martial",
    "nepos",
    "livy",
    "tacitus",
    "quintilian",
    "suetonius",
    "apuleius",
    "sen"
]
AUTHOR_TXTS = {
    "catullus": ["catullus.txt"],
    "propertius": ["propertius1.txt"],
    "tibullus": ["tibullus1.txt", "tibullus2.txt", "tibullus3.txt"],
    "persius": ["persius.txt"],
    "sallust": ["sall.1.txt", "sall.2.txt"],
    "petronius": ["petronius.txt", "petronius1.txt"],
    "pliny_younger": [
        "pliny.ep1.txt",
        "pliny.ep2.txt",
        "pliny.ep3.txt",
        "pliny.ep4.txt",
        "pliny.ep5.txt",
        "pliny.ep6.txt",
        "pliny.ep7.txt",
        "pliny.ep8.txt",
        "pliny.ep9.txt",
        "pliny.ep10.txt",
        "pliny.panegyricus.txt"
    ]
}


if __name__ == "__main__":
    base_path = "/Users/tyler/cltk_data/latin/text/latin_text_latin_library/"
    corpora = {}
    for a in AUTHOR_DIRS:
        author_dir = base_path + a
        texts = [author_dir+"/"+t for t in os.listdir(author_dir) if t[-3:] == "txt"]
        corpora[a] = texts
    for k, v in AUTHOR_TXTS.items():
        texts = [base_path+t for t in v]
        corpora[k] = texts
    with open(f"../assets/{CORPUS_NAME}_corpora.json", "w") as f:
        json.dump(corpora, f, indent=4, sort_keys=True)
