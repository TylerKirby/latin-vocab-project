import re
from collections import Counter
from dataclasses import dataclass
from itertools import chain
from typing import Dict, List, Tuple

from cltk.lemmatize.lat import LatinBackoffLemmatizer
from cltk.ner.ner import tag_ner
from cltk.sentence.lat import LatinPunktSentenceTokenizer


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
            self.sent_tokenizer = LatinPunktSentenceTokenizer()

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
        Reduces secondary definitions to single lemma. E.g., all "cum2" counts are under "cum".
        :param lemmata: list of lemmata tuples
        :return: dict of lemmata frequency
        """
        freq_dict_temp = dict(Counter([l[1] for l in lemmata]))
        freq_dict = {}
        for k, v in freq_dict_temp.items():
            if k[-1].isnumeric():
                try:
                    freq_dict[k[:-1]] += v
                except KeyError:
                    freq_dict[k[:-1]] = v
            else:
                try:
                    freq_dict[k] += v
                except KeyError:
                    freq_dict[k] = v
        return freq_dict

    def ner_tagger(self, text: str, use_spacy=True) -> List[Tuple[str, bool]]:
        """
        Tag named entities in text.
        :param text: text
        :param use_spacy: flag to use Spacy NER tagger. Note that it runs slowly.
        :return: list of booleans - true indicates named entity
        """
        sentences = self.sent_tokenizer.tokenize(text)
        tagged_sentences = []
        for sentence in sentences:
            tokens = sentence.split(" ")
            if use_spacy:
                cltk_ner_tags = tag_ner(iso_code="lat", input_tokens=tokens)
            else:
                cltk_ner_tags = tokens
            ner_tags = []
            for i in range(len(cltk_ner_tags)):
                if i == 0:
                    ner_tags.append((tokens[i], cltk_ner_tags[i] == True))
                elif tokens[i][0].isupper():
                    ner_tags.append((tokens[i], True))
                else:
                    ner_tags.append((tokens[i], cltk_ner_tags[i] == True))
            tagged_sentences.append(ner_tags)
        tagged_text = list(chain.from_iterable(tagged_sentences))
        return tagged_text

    def process_text(self, text: str, filter_ner=True) -> ProcessedText:
        """
        Collates text, clean text, lemmata, and lemmata frequencies for text.
        :param text: raw Latin Library text
        :return: processed Latin Library text
        """
        clean_text = self.clean_text(text, lower=True)
        text_title = text.split("\n")[0]
        only_alphabetic_pattern = re.compile("[^a-z]")
        clean_tokens = [
            only_alphabetic_pattern.sub("", t) for t in clean_text.split(" ")
        ]  # Remove punc from tokens
        lemmata = self.lemmatizer.lemmatize(clean_tokens)
        if filter_ner:
            clean_text_ner = self.clean_text(text, lower=False)
            ner_tags = self.ner_tagger(clean_text_ner, use_spacy=False)
            filter_lemmata = [
                t[0] for t in zip(lemmata, ner_tags) if t[1][1] is not True
            ]
            lemmata_frequencies = self.lemmata_freq(filter_lemmata)
        else:
            lemmata_frequencies = self.lemmata_freq(lemmata)
        processed_text = ProcessedText(
            title=text_title,
            raw_text=text,
            clean_text=clean_text,
            lemmata=lemmata,
            lemmata_frequencies=lemmata_frequencies,
        )
        return processed_text

    def process_corpus(self, texts: List[str]) -> Dict[str, int]:
        """
        Processes a list of texts into a single cumulative frequency dictionary.
        :param texts: list of absolute paths to Latin Library texts
        """
        lemmata_frequencies = []
        for text_path in texts:
            with open(text_path, "r") as f:
                text = f.read()
            lemmata_frequencies.append(self.process_text(text).lemmata_frequencies)
        cumulative_freq = {}
        for freq in lemmata_frequencies:
            for k, v in freq.items():
                if k in cumulative_freq:
                    cumulative_freq[k] += v
                else:
                    cumulative_freq[k] = v
        return cumulative_freq
