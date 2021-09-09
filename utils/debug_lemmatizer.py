from cltk.lemmatize.lat import LatinBackoffLemmatizer


if __name__ == '__main__':
    lemmatizer = LatinBackoffLemmatizer(verbose=True)
    text = """Et
uti eo introeas et circumspicias, uti inde exire possis. Uti bonum caelum
habeat; ne calamitosum siet; solo bono, sua virtute valeat. Si poteris,"""
    lemma = lemmatizer.lemmatize(text.split())
    print(lemma)
