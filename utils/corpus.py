import re
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Tuple

from cltk.lemmatize.lat import LatinBackoffLemmatizer


@dataclass
class ProcessedText:
    title: str
    raw_text: str
    clean_text: str
    lemmata: List[Tuple[str, str]]
    tokenized_lemmata: List[str]
    lemmata_frequencies: Dict[str, int]


class CorpusAnalytics:
    def __init__(self, lang):
        if lang == "lat":
            self.lemmatizer = LatinBackoffLemmatizer()

    def process(self, text: str) -> ProcessedText:
        """
        Collates text, clean text, lemmata, and lemmata frequencies for text.
        :param text: raw Latin Library text
        :return: processed Latin Library text
        """

        pattern = re.compile("\s\s+")
        clean_text = pattern.sub(" ", text).strip()
        text_title = text.split("\n")[0]
        lemmata = self.lemmatizer.lemmatize(clean_text.split(" "))
        lemmata = [l for l in lemmata if l[1] != ""]
        tokenized_lemmata = [t[1] for t in lemmata]
        processed_text = ProcessedText(
            title=text_title,
            raw_text=text,
            clean_text=clean_text,
            lemmata=lemmata,
            tokenized_lemmata=tokenized_lemmata,
            lemmata_frequencies=Counter(tokenized_lemmata),
        )
        return processed_text

    def process_corpus(self, texts: List[str]) -> List[ProcessedText]:
        """
        Processes a list of texts.
        :param texts: list of absolute paths to Latin Library texts
        """
        processed_texts = []
        for text_path in texts:
            with open(text_path, "r") as f:
                text = f.read()
            processed_texts.append(self.process(text))
        return processed_texts
