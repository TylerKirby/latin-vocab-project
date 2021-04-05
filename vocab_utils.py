import re
from string import punctuation
from collections import Counter
from cltk.ner.ner import tag_ner
from cltk.lemmatize.lat import LatinBackoffLemmatizer


class CorpusAnalytics:
    def __init__(self, texts, texts_path, lang):
        self.texts = texts

        if lang == "lat":
            lemmatizer = LatinBackoffLemmatizer()

        pattern = re.compile('[^a-zA-Z]')
        self.analytics = {}
        for text in texts:
            text_path = texts_path + text
            with open(text_path) as file:
                raw_text = file.read()
            clean_text = pattern.sub(' ', raw_text).strip()
            text_title = text[:-4]
            lemmata = lemmatizer.lemmatize(clean_text.split(" "))
            lemmata = [l for l in lemmata if l[1] != '']
            tokenized_lemmata = [t[1] for t in lemmata]
            ner_tags = list(zip(tokenized_lemmata, tag_ner("lat", tokenized_lemmata)))  # NER tagger requires capitalization to be preserved
            ner_filtered_tags = [t[0].lower() for t in ner_tags if not t[1]]
            ners = [t[0].lower() for t in ner_tags if t[1]]
            self.analytics[text_title] = {
                "clean_text": clean_text,
                "lemmata": lemmata,
                "tokenized_lemmata": tokenized_lemmata,
                "lemmata_frequencies": Counter(tokenized_lemmata),
                "filtered_lemmata_frequencies": Counter(ner_filtered_tags),
                "ner_filtered_tokens": ner_filtered_tags,
                "ners": ners
            }

with open("diederich.txt") as f:
    diederich_vocab_raw = [l.split(";")[0] for l in f.readlines()[3:]]
diederich_vocab = []
for v in diederich_vocab_raw:
    if ' ' in v:
        v = v.split(" ")[0]
    v = v.strip(punctuation)
    diederich_vocab.append(v)


if __name__ == "__main__":
    ap_latin_texts = [
        "vergil/aen1.txt",
        "vergil/aen2.txt",
        "vergil/aen4.txt",
        "vergil/aen6.txt",
        "caesar/gall1.txt",
        "caesar/gall4.txt",
        "caesar/gall5.txt",
        "caesar/gall6.txt"
    ]
    path_to_texts = "/Users/tyler/cltk_data/latin/text/latin_text_latin_library/"
    ap_latin_corpus = CorpusAnalytics(ap_latin_texts, path_to_texts, "lat")
    pass
