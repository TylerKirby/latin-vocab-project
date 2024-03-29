"""
Create JSON of authors and text paths.
"""

import json
import os

CORPUS_NAME = "classical"
AUTHOR_DIRS = [
    "vergil",
    "cicero",
    "curtius",
    "frontinus",
    "horace",
    "ovid",
    "lucan",
    "juvenal",
    "martial",
    "nepos",
    "livy",
    "tacitus",
    "suetonius",
    "apuleius",
    "sen",
    "silius",
    "statius",
    "columella",
    "hyginus",
]
AUTHOR_TXTS = {
    "manilius": [
        "manilius1.txt",
        "manilius2.txt",
        "manilius3.txt",
        "manilius4.txt",
        "manilius5.txt",
    ],
    "pomponius_mela": ["pomponius1.txt", "pomponius2.txt", "pomponius3.txt"],
    "carmina_pripea": ["priapea.txt"],
    "ilias_latina": ["ilias.txt"],
    "germanicus": ["germanicus.txt"],
    "grattius": ["grattius.txt"],
    "valerius_flaccus": [
        "valeriusflaccus1.txt",
        "valeriusflaccus2.txt",
        "valeriusflaccus3.txt",
        "valeriusflaccus4.txt",
        "valeriusflaccus5.txt",
        "valeriusflaccus6.txt",
        "valeriusflaccus7.txt",
        "valeriusflaccus8.txt",
    ],
    "valerius_maximus": [
        "valmax1.txt",
        "valmax2.txt",
        "valmax3.txt",
        "valmax4.txt",
        "valmax5.txt",
        "valmax6.txt",
        "valmax7.txt",
        "valmax8.txt",
        "valmax9.txt",
    ],
    "varro": [
        "varro.rr1.txt",
        "varro.rr2.txt",
        "varro.rr3.txt",
        "varro.ll5.txt",
        "varro.ll6.txt",
        "varro.ll7.txt",
        "varro.ll8.txt",
        "varro.ll9.txt",
        "varro.ll10.txt",
        "varro.frag.txt",
    ],
    "vellius": ["vell1.txt", "vell2.txt"],
    "vitruvius": [
        "vitruvius1.txt",
        "vitruvius2.txt",
        "vitruvius3.txt",
        "vitruvius4.txt",
        "vitruvius5.txt",
        "vitruvius6.txt",
        "vitruvius7.txt",
        "vitruvius8.txt",
        "vitruvius9.txt",
        "vitruvius10.txt",
    ],
    "calpurnius_siculus": ["calpurniussiculus.txt"],
    "asconius": ["asconius.txt"],
    "suplpicia": ["sulpicia.txt"],
    "aug_res_gestae": ["resgestae.txt"],
    "caesar": [
        "caesar/gall1.txt",
        "caesar/gall2.txt",
        "caesar/gall3.txt",
        "caesar/gall4.txt",
        "caesar/gall5.txt",
        "caesar/gall6.txt",
        "caesar/gall7.txt",
        "caesar/bc1.txt",
        "caesar/bc2.txt",
        "caesar/bc3.txt",
    ],
    "corpus_caesarianum": [
        "caesar/gall8.txt",
        "caesar/hisp.txt",
        "caesar/bellafr.txt",
        "caesar/alex.txt",
    ],
    "pliny_maior": [
        "pliny.nh1.txt",
        "pliny.nh2.txt",
        "pliny.nh3.txt",
        "pliny.nh4.txt",
        "pliny.nh5.txt",
        "pliny.nhpr.txt",
    ],
    "seneca_maior": [
        "seneca.contr1.txt",
        "seneca.contr2.txt",
        "seneca.contr3.txt",
        "seneca.contr4.txt",
        "seneca.contr5.txt",
        "seneca.contr6.txt",
        "seneca.contr7.txt",
        "seneca.contr8.txt",
        "seneca.contr9.txt",
        "seneca.contr10.txt",
        "seneca.contr11.txt",
        "seneca.fragmenta.txt",
        "seneca.suasoriae.txt",
    ],
    "quintilian_inst": [
        "quintilian/quintilian.institutio1.txt",
        "quintilian/quintilian.institutio2.txt",
        "quintilian/quintilian.institutio3.txt",
        "quintilian/quintilian.institutio4.txt",
        "quintilian/quintilian.institutio5.txt",
        "quintilian/quintilian.institutio6.txt",
        "quintilian/quintilian.institutio7.txt",
        "quintilian/quintilian.institutio8.txt",
        "quintilian/quintilian.institutio9.txt",
        "quintilian/quintilian.institutio10.txt",
        "quintilian/quintilian.institutio11.txt",
        "quintilian/quintilian.institutio12.txt",
    ],
    "quintilian_decl_mai": [
        "quintilian/quintilian.decl.mai1.txt",
        "quintilian/quintilian.decl.mai2.txt",
        "quintilian/quintilian.decl.mai3.txt",
        "quintilian/quintilian.decl.mai4.txt",
        "quintilian/quintilian.decl.mai5.txt",
        "quintilian/quintilian.decl.mai6.txt",
        "quintilian/quintilian.decl.mai7.txt",
        "quintilian/quintilian.decl.mai8.txt",
        "quintilian/quintilian.decl.mai9.txt",
        "quintilian/quintilian.decl.mai10.txt",
        "quintilian/quintilian.decl.mai11.txt",
        "quintilian/quintilian.decl.mai12.txt",
        "quintilian/quintilian.decl.mai13.txt",
        "quintilian/quintilian.decl.mai14.txt",
        "quintilian/quintilian.decl.mai15.txt",
        "quintilian/quintilian.decl.mai16.txt",
        "quintilian/quintilian.decl.mai17.txt",
        "quintilian/quintilian.decl.mai18.txt",
        "quintilian/quintilian.decl.mai19.txt",
    ],
    "catullus": ["catullus.txt"],
    "propertius": ["propertius1.txt", "prop2.txt", "prop3.txt", "prop4.txt"],
    "tibullus": ["tibullus1.txt", "tibullus2.txt", "tibullus3.txt"],
    "persius": ["persius.txt"],
    "sallust": ["sall.1.txt", "sall.2.txt"],
    "petronius": ["petronius.txt", "petronius1.txt", "petroniusfrag.txt"],
    "pliny_younger": [
        "pliny.ep1.txt",
        "pliny.ep2.txt",
        "pliny.ep3.txt",
        "pliny.ep4.txt",
        "pliny.ep5.txt",
        "pliny.ep6.txt",
        "pliny.ep7.txt",
        "pliny.ep8.txt",
        "pliny.ep9.txt",
        "pliny.ep10.txt",
        "pliny.panegyricus.txt",
    ],
}


if __name__ == "__main__":
    base_path = "/Users/tyler/cltk_data/latin/text/latin_text_latin_library/"
    corpora = {}
    for a in AUTHOR_DIRS:
        author_dir = base_path + a
        texts = [
            author_dir + "/" + t for t in os.listdir(author_dir) if t[-3:] == "txt"
        ]
        corpora[a] = texts
    for k, v in AUTHOR_TXTS.items():
        texts = [base_path + t for t in v]
        corpora[k] = texts
    with open(f"../assets/{CORPUS_NAME}_corpora.json", "w") as f:
        json.dump(corpora, f, indent=4, sort_keys=True)
