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
    lemmata_frequencies: Dict[str, int]


class CorpusAnalytics:
    def __init__(self, lang):
        if lang == "lat":
            self.lemmatizer = LatinBackoffLemmatizer()

    @staticmethod
    def clean_text(text: str, lower: bool = False) -> str:
        """
        Remove extra punctuation and white space.
        Optionally lower case text
        :param text: raw text
        :param lower: whether to lower case text
        :return: clean text
        """
        # Remove non end of sentence punctuation
        punc_pattern = re.compile("[^a-zA-Z.?!\s]")
        clean_text = punc_pattern.sub("", text)
        # Remove duplicate white space
        duplicate_white_space_pattern = re.compile("\s\s+")
        clean_text = duplicate_white_space_pattern.sub(" ", clean_text).strip()
        # Replace non period end of sentence punc with period
        eos_pattern = re.compile("[!?]")
        clean_text = eos_pattern.sub(".", clean_text)
        if lower:
            return clean_text.lower()
        return clean_text

    @staticmethod
    def lemmata_freq(lemmata: List[Tuple[str, str]]) -> Dict[str, int]:
        """
        Collate lemmata for vocab frequency.
        :param lemmata: list of lemmata tuples
        :return: dict of lemmata frequency
        """
        return dict(Counter([l[1] for l in lemmata]))

    def process_text(self, text: str) -> ProcessedText:
        """
        Collates text, clean text, lemmata, and lemmata frequencies for text.
        :param text: raw Latin Library text
        :return: processed Latin Library text
        """
        clean_text = self.clean_text(text, lower=True)
        text_title = text.split("\n")[0]
        lemmata = self.lemmatizer.lemmatize(clean_text.split(" "))
        lemmata_frequencies = self.lemmata_freq(lemmata)
        processed_text = ProcessedText(
            title=text_title,
            raw_text=text,
            clean_text=clean_text,
            lemmata=lemmata,
            lemmata_frequencies=lemmata_frequencies,
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
            processed_texts.append(self.process_text(text))
        return processed_texts
