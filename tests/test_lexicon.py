from modules import Lexicon, LexiconOptions


def test_lexicon_freq():
    opts = LexiconOptions("freq", 3)
    test_lex = Lexicon("tests/test_freq_table.csv", opts)
    assert len(test_lex.lexicon) == 3


def test_lexicon_perc():
    opts = LexiconOptions("perc", 0.3)
    test_lex = Lexicon("tests/test_freq_table.csv", opts)
    assert len(test_lex.lexicon) == 5
