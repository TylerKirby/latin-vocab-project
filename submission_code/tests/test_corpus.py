from cltk.data.fetch import FetchCorpus

from submission_code.modules import CorpusAnalytics

corpus_downloader = FetchCorpus(language="lat")
corpus_downloader.import_corpus("lat_models_cltk")

with open("tests/aen1.txt", "r") as f:
    text = f.read()

cltk_analytics = CorpusAnalytics("lat", lemmatizer_type="cltk")


def test_process_text_title():
    vergil_1 = cltk_analytics.process_text(text)
    correct = "Vergil: Aeneid I"
    assert vergil_1.title == correct


def test_process_text_raw_text():
    vergil_1 = cltk_analytics.process_text(text)
    correct = "Vergil: Aeneid I"
    assert vergil_1.raw_text[: len(correct)] == correct


def test_process_text_clean_text():
    vergil_1 = cltk_analytics.process_text(text)
    correct = "uergil aeneid i p. uergili"
    assert vergil_1.clean_text[: len(correct)] == correct


def test_process_text_lemmata():
    vergil_1 = cltk_analytics.process_text(text)
    correct = [("arma", "arma"), ("uirumque", "vir"), ("cano", "cano")]
    assert vergil_1.lemmata[9:12] == correct


def test_clean_text():
    sample = "Vergil   Aeneid &#26 Arma: virumque, cano?"
    correct = "Uergil Aeneid Arma uirumque cano."
    assert cltk_analytics.clean_text(sample) == correct


def test_lemmata_freq():
    sample = [("vergil", "vergil"), ("vergil", "vergil"), ("et", "et")]
    correct = {"uergil": 2, "et": 1}
    assert cltk_analytics.lemmata_freq(sample) == correct


def test_lemmata_freq_hyphenate():
    sample = [("convero", "con-vero"), ("convero", "convero")]
    correct = {"conuero": 2}
    assert cltk_analytics.lemmata_freq(sample) == correct
    sample = [("convero", "con-vero")]
    correct = {"conuero": 1}
    assert cltk_analytics.lemmata_freq(sample) == correct


def test_lemmata_freq_aris_forms():
    sample = [("fateor", "fateor"), ("fatearis", "fatearis")]
    correct = {"fateor": 2}
    assert cltk_analytics.lemmata_freq(sample) == correct


def test_lemmata_freq_no_numbers():
    sample = [("cum", "cum2"), ("cum", "cum2"), ("cum", "cum")]
    correct = {"cum": 3}
    assert cltk_analytics.lemmata_freq(sample) == correct
    sample = [("cum", "cum2"), ("cum", "cum2")]
    correct = {"cum": 2}
    assert cltk_analytics.lemmata_freq(sample) == correct


def test_lemmata_freq_exclude():
    sample = [("aeumlre", "aeumlre")]
    correct = {}
    assert cltk_analytics.lemmata_freq(sample) == correct


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
    assert cltk_analytics.ner_tagger(sample) == correct


def test_process_corpus():
    test_texts = [
        "tests/test_text1.txt",
        "tests/test_text2.txt",
    ]
    actual = cltk_analytics.process_corpus(test_texts)
    correct = {"quo": 2, "abutor": 2, "patientia": 2, "nos": 1}
    assert actual == correct


def test_is_numeral():
    # Case 1: is not a numeral, contains no numerals
    actual = cltk_analytics.is_numeral("puer")
    correct = False
    assert actual == correct
    # Case 2: is not a numeral, contains a numeral
    assert cltk_analytics.is_numeral("vis") == False
    assert cltk_analytics.is_numeral("vergil") == False
    # Case 3: is a numeral, not vix
    actual = cltk_analytics.is_numeral("c")
    correct = True
    assert actual == correct
    # Case 4: is a numeral, is vix
    actual = cltk_analytics.is_numeral("vix")
    correct = False
    assert actual == correct


def test_clean_lemma_no_que():
    actual = cltk_analytics.clean_lemma("puerque")
    correct = "puer"
    assert actual == correct
    actual = cltk_analytics.clean_lemma("ubique")
    correct = "ubique"
    assert actual == correct


def test_clean_lemma_no_ve():
    actual = cltk_analytics.clean_lemma("puerve")
    correct = "puer"
    assert actual == correct
    actual = cltk_analytics.clean_lemma("graue")
    correct = "graue"
    assert actual == correct
    actual = cltk_analytics.clean_lemma("puerue")
    correct = "puer"
    assert actual == correct


def test_clean_lemmata_e_ex():
    actual = cltk_analytics.clean_lemma("e")
    correct = "ex"
    assert actual == correct


lamonpy_analytics = CorpusAnalytics("lat", lemmatizer_type="lamonpy")


def test_basic_test_lamonpy():
    sample_text = """
    Bello Alexandrino conflato Caesar Rhodo atque ex Syria Ciliciaque omnem classem arcessit; Creta sagittarios, 
    equites ab rege Nabataeorum Malcho evocat; tormenta undique conquiri et frumentum mitti, auxilia adduci iubet. 
    Interim munitiones cotidie operibus augentur atque omnes oppidi partes, quae minus esse firmae videntur, 
    testudinibus ac musculis +aptantur+; ex aedificiis autem per foramina in proxima aedificia arietes immittuntur, 
    quantumque aut ruinis deicitur aut per vim recipitur loci, in tantum munitiones proferuntur. Nam incendio fere tuta 
    est Alexandrea, quod sine contignatione ac materia sunt aedificia et structuris ac fornicibus continentur tectaque 
    sunt rudere aut pavimentis.
    """
    actual = lamonpy_analytics.process_text(sample_text, filter_ner=False)
    correct_clean_text = "bello alexandrino conflato caesar rhodo atque ex syria ciliciaque omnem classem arcessit creta sagittarios equites ab rege nabataeorum malcho euocat tormenta undique conquiri et frumentum mitti auxilia adduci iubet. interim munitiones cotidie operibus augentur atque omnes oppidi partes quae minus esse firmae uidentur testudinibus ac musculis aptantur ex aedificiis autem per foramina in proxima aedificia arietes immittuntur quantumque aut ruinis deicitur aut per uim recipitur loci in tantum munitiones proferuntur. nam incendio fere tuta est alexandrea quod sine contignatione ac materia sunt aedificia et structuris ac fornicibus continentur tectaque sunt rudere aut pauimentis."
    correct_lemmata = [
        ("", "bellum"),
        ("", "alexandrinus"),
        ("", "conflo"),
        ("", "Caesar"),
        ("", "Rhodus"),
        ("", "atque"),
        ("", "ex"),
        ("", "[UNK]"),
        ("", "cilicium"),
        ("", "omnis"),
        ("", "classis"),
        ("", "arcesso"),
        ("", "creta"),
        ("", "sagittarius"),
        ("", "eques"),
        ("", "ab"),
        ("", "rex"),
        ("", "[UNK]"),
        ("", "[UNK]"),
        ("", "evoco"),
        ("", "tormentum"),
        ("", "undique"),
        ("", "conquiro"),
        ("", "et"),
        ("", "frumentum"),
        ("", "mitto"),
        ("", "auxilium"),
        ("", "adduco"),
        ("", "iubeo"),
        ("", "."),
        ("", "interim"),
        ("", "munitio"),
        ("", "cotidie"),
        ("", "opus"),
        ("", "augeo"),
        ("", "atque"),
        ("", "omnis"),
        ("", "oppidum"),
        ("", "pars"),
        ("", "qui"),
        ("", "parum"),
        ("", "edo"),
        ("", "firmus"),
        ("", "video"),
        ("", "testudo"),
        ("", "ac"),
        ("", "musculus"),
        ("", "apto"),
        ("", "ex"),
        ("", "aedificium"),
        ("", "autem"),
        ("", "per"),
        ("", "foramen"),
        ("", "in"),
        ("", "propior"),
        ("", "aedificium"),
        ("", "aries"),
        ("", "immitto"),
        ("", "quantum"),
        ("", "aut"),
        ("", "ruina"),
        ("", "deicio"),
        ("", "aut"),
        ("", "per"),
        ("", "vis"),
        ("", "recipio"),
        ("", "locus"),
        ("", "in"),
        ("", "tantus"),
        ("", "munitio"),
        ("", "profero"),
        ("", "."),
        ("", "nam"),
        ("", "incendium"),
        ("", "fere"),
        ("", "tutus"),
        ("", "sum"),
        ("", "[UNK]"),
        ("", "quod"),
        ("", "sine"),
        ("", "contignatio"),
        ("", "ac"),
        ("", "materia"),
        ("", "sum"),
        ("", "aedificium"),
        ("", "et"),
        ("", "structura"),
        ("", "ac"),
        ("", "fornix"),
        ("", "contineo"),
        ("", "tectum"),
        ("", "sum"),
        ("", "rudus"),
        ("", "aut"),
        ("", "pavimentum"),
        ("", "."),
    ]
    correct_lemmata_frequencies = {
        "bellum": 1,
        "alexandrinus": 1,
        "conflo": 1,
        "caesar": 1,
        "rhodus": 1,
        "atque": 2,
        "ex": 2,
        "cilicium": 1,
        "omnis": 2,
        "classis": 1,
        "arcesso": 1,
        "creta": 1,
        "sagittarius": 1,
        "eques": 1,
        "ab": 1,
        "rex": 1,
        "euoco": 1,
        "tormentum": 1,
        "undique": 1,
        "conquiro": 1,
        "et": 2,
        "frumentum": 1,
        "mitto": 1,
        "auxilium": 1,
        "adduco": 1,
        "iubeo": 1,
        "interim": 1,
        "munitio": 2,
        "cotidie": 1,
        "opus": 1,
        "augeo": 1,
        "oppidum": 1,
        "pars": 1,
        "qui": 1,
        "parum": 1,
        "edo": 1,
        "firmus": 1,
        "uideo": 1,
        "testudo": 1,
        "ac": 3,
        "musculus": 1,
        "apto": 1,
        "aedificium": 3,
        "autem": 1,
        "per": 2,
        "foramen": 1,
        "in": 2,
        "propior": 1,
        "aries": 1,
        "immitto": 1,
        "quantum": 1,
        "aut": 3,
        "ruina": 1,
        "deicio": 1,
        "uis": 1,
        "recipio": 1,
        "locus": 1,
        "tantus": 1,
        "profero": 1,
        "nam": 1,
        "incendium": 1,
        "fere": 1,
        "tutus": 1,
        "sum": 3,
        "quod": 1,
        "sine": 1,
        "contignatio": 1,
        "materia": 1,
        "structura": 1,
        "fornix": 1,
        "contineo": 1,
        "tectum": 1,
        "rudus": 1,
        "pauimentum": 1,
    }
    assert actual.clean_text == correct_clean_text
    assert actual.lemmata == correct_lemmata
    assert actual.lemmata_frequencies == correct_lemmata_frequencies


def test_lamonpy_sui_issue():
    actual = lamonpy_analytics.process_text("suus sui")
    correct = {"suus": 2}
    assert actual.lemmata_frequencies == correct


def test_lamonpy_p():
    actual = lamonpy_analytics.process_text("P. amo puellam.", filter_ner=True)
    correct = {"amo": 1, "puella": 1}
