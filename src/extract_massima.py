# Based on https://stackoverflow.com/a/62859169/562769

from typing import List, Tuple

import fitz  # install with 'pip install pymupdf'

'''
    Recupera il quadrato geometrico che racchiude l'annotazione e ne 
    fa l'intersezione con la lista delle parole in modo da recuperare 
    le parole effettive che compaiono all'interno di quel quadrato
'''
def _parse_highlight(annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
    points = annot.vertices
    quad_count = int(len(points) / 4)
    sentences = []
    for i in range(quad_count):
        # where the highlighted part is
        r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect

        words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
        sentences.append(" ".join(w[4] for w in words))
    sentence = " ".join(sentences)
    return sentence

''' 
    Per ogni pagina, recupera la lista di tutte le parole e
    e se trova delle annotazioni di tipo 8 (ovvero evidenziatore)
    ne passa il contenuto alla funzione _parse_highlight insieme 
    alla lista di tutte le parole
'''
def handle_page(page):
    wordlist = page.get_text("words")  # list of words on page
    wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x

    highlights = []
    annot = page.firstAnnot
    while annot:
        print(annot.colors)
        if annot.type[0] == 8:
            highlights.append(_parse_highlight(annot, wordlist))
        annot = annot.next
    return highlights

# Apre il PDF e ne analizza il contenuto per ogni pagina
def main(filepath: str) -> List:
    doc = fitz.open(filepath)

    highlights = []
    for page in doc:
        highlights += handle_page(page)

    return highlights


if __name__ == "__main__":
    highlights = main("docs2/Sent 179-2021.pdf")
    print(" \n".join(highlights))