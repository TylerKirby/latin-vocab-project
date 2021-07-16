from utils.corpus import CorpusAnalytics

with open(
    "/Users/tyler/cltk_data/latin/text/latin_text_latin_library/vergil/aen1.txt", "r"
) as f:
    text = f.read()

analytics = CorpusAnalytics("lat")
vergil_1 = analytics.process_text(text)


def test_process_text_title():
    correct = "Vergil: Aeneid I"
    assert vergil_1.title == correct


def test_process_text_raw_text():
    correct = "Vergil: Aeneid I\n\t\t \n\n\t"
    assert vergil_1.raw_text[: len(correct)] == correct


def test_process_text_clean_text():
    correct = "vergil aeneid i p. vergili"
    assert vergil_1.clean_text[: len(correct)] == correct


def test_process_text_lemmata():
    correct = [("arma", "arma"), ("virumque", "vir"), ("cano", "cano")]
    assert vergil_1.lemmata[9:12] == correct


def test_clean_text():
    sample = "Vergil   Aeneid &#26 Arma: virumque, cano?"
    correct = "Vergil Aeneid Arma virumque cano."
    assert analytics.clean_text(sample) == correct


def test_lemmata_freq():
    sample = [("vergil", "vergil"), ("vergil", "vergil"), ("et", "et")]
    correct = {"vergil": 2, "et": 1}
    assert analytics.lemmata_freq(sample) == correct
