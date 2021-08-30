from utils.corpus import CorpusAnalytics

with open(
    "/Users/tyler/cltk_data/latin/text/latin_text_latin_library/vergil/aen1.txt", "r"
) as f:
    text = f.read()

analytics = CorpusAnalytics("lat")


def test_process_text_title():
    vergil_1 = analytics.process_text(text)
    correct = "Vergil: Aeneid I"
    assert vergil_1.title == correct


def test_process_text_raw_text():
    vergil_1 = analytics.process_text(text)
    correct = "Vergil: Aeneid I\n\t\t \n\n\t"
    assert vergil_1.raw_text[: len(correct)] == correct


def test_process_text_clean_text():
    vergil_1 = analytics.process_text(text)
    correct = "uergil aeneid i p. uergili"
    assert vergil_1.clean_text[: len(correct)] == correct


def test_process_text_lemmata():
    vergil_1 = analytics.process_text(text)
    correct = [("arma", "arma"), ("uirumque", "vir"), ("cano", "cano")]
    assert vergil_1.lemmata[9:12] == correct


def test_clean_text():
    sample = "Vergil   Aeneid &#26 Arma: virumque, cano?"
    correct = "Uergil Aeneid Arma uirumque cano."
    assert analytics.clean_text(sample) == correct


def test_lemmata_freq():
    sample = [("vergil", "vergil"), ("vergil", "vergil"), ("et", "et")]
    correct = {"uergil": 2, "et": 1}
    assert analytics.lemmata_freq(sample) == correct


def test_lemmata_freq_hyphenate():
    sample = [("convero", "con-vero"), ("convero", "convero")]
    correct = {"conuero": 2}
    assert analytics.lemmata_freq(sample) == correct
    sample = [("convero", "con-vero")]
    correct = {"conuero": 1}
    assert analytics.lemmata_freq(sample) == correct


def test_lemmata_freq_aris_forms():
    sample = [("fateor", "fateor"), ("fatearis", "fatearis")]
    correct = {"fateor": 2}
    assert analytics.lemmata_freq(sample) == correct


def test_lemmata_freq_no_numbers():
    sample = [("cum", "cum2"), ("cum", "cum2"), ("cum", "cum")]
    correct = {"cum": 3}
    assert analytics.lemmata_freq(sample) == correct
    sample = [("cum", "cum2"), ("cum", "cum2")]
    correct = {"cum": 2}
    assert analytics.lemmata_freq(sample) == correct


def test_lemmata_freq_exclude():
    sample = [("aeumlre", "aeumlre")]
    correct = {}
    assert analytics.lemmata_freq(sample) == correct


def test_ner_tagger():
    sample = (
        "Arma virumque cano Sequano Caesar flumen. Pallasne exurere classem Argivom atque ipsos potuit "
        "submergere ponto unius ob noxam et furias Aiacis Oilei."
    )
    correct = [
        ("Arma", False),
        ("virumque", False),
        ("cano", False),
        ("Sequano", True),
        ("Caesar", True),
        ("flumen.", False),
        (
            "Pallasne",
            False,
        ),  # Beginning of second sentence and cltk tagger does not detect it correctly.
        ("exurere", False),
        ("classem", False),
        ("Argivom", True),
        ("atque", False),
        ("ipsos", False),
        ("potuit", False),
        ("submergere", False),
        ("ponto", False),
        ("unius", False),
        ("ob", False),
        ("noxam", False),
        ("et", False),
        ("furias", False),
        ("Aiacis", True),
        ("Oilei.", True),
    ]
    assert analytics.ner_tagger(sample) == correct


def test_process_corpus():
    test_texts = [
        "/Users/tyler/Projects/latin-vocab-project/tests/test_text1.txt",
        "/Users/tyler/Projects/latin-vocab-project/tests/test_text2.txt",
    ]
    actual = analytics.process_corpus(test_texts)
    correct = {"quo": 2, "abutor": 2, "patientia": 2, "nos": 1}
    assert actual == correct


def test_is_numeral():
    # Case 1: is not a numeral, contains no numerals
    actual = analytics.is_numeral("puer")
    correct = False
    assert actual == correct
    # Case 2: is not a numeral, contains a numeral
    assert analytics.is_numeral("vis") == False
    assert analytics.is_numeral("vergil") == False
    # Case 3: is a numeral, not vix
    actual = analytics.is_numeral("c")
    correct = True
    assert actual == correct
    # Case 4: is a numeral, is vix
    actual = analytics.is_numeral("vix")
    correct = False
    assert actual == correct


def test_clean_lemma_no_que():
    actual = analytics.clean_lemma("puerque")
    correct = "puer"
    assert actual == correct
    actual = analytics.clean_lemma("ubique")
    correct = "ubique"
    assert actual == correct
