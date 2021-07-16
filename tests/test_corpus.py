from utils.corpus import CorpusAnalytics

sample_corpus = [
    "/Users/tyler/cltk_data/latin/text/latin_text_latin_library/vergil/aen1.txt"
]
analytics = CorpusAnalytics("lat")
processed_texts = analytics.process_corpus(sample_corpus)
vergil_1 = processed_texts[0]


def test_process_text_title():
    correct = "Vergil: Aeneid I"
    assert vergil_1.title == correct


def test_process_text_raw_text():
    correct = "Vergil: Aeneid I\n\t\t \n\n\t"
    assert vergil_1.raw_text[: len(correct)] == correct


def test_process_text_clean_text():
    correct = "Vergil: Aeneid I P. VERGILI"
    assert vergil_1.clean_text[: len(correct)] == correct
