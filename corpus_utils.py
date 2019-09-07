from cltk.corpus.utils.importer import CorpusImporter


def list_corpora(lang='latin'):
    corpus_importer = CorpusImporter(lang)
    return corpus_importer.list_corpora


def download_corpus(corpus, lang='latin'):
    corpus_importer = CorpusImporter(lang)
    corpus_importer.import_corpus(corpus)


if __name__ == '__main__':
    download_corpus('latin_text_perseus')

