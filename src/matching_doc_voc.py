from elasticsearch import Elasticsearch
import PyPDF2
from datetime import datetime
import nltk
import os
import string
from nltk.corpus import stopwords

# Scarica dal natural language toolkit i segni di punteggiatura e le stopwords
nltk.download("punkt")
nltk.download("stopwords")

# Recupero le stopwords italiane
italian_stopwords = stopwords.words("italian")

path = os.getcwd()

# Leggo i diversi PDF nella mia banca dati: sarà un loop su tutti i documenti
reader = PyPDF2.PdfFileReader("docs/39-2021 evidenziata.pdf")
reader2 = PyPDF2.PdfFileReader("docs/sent. 103 - 2021 v.pdf")

number_of_pages1 = len(reader.pages)
number_of_pages2 = len(reader2.pages)

# Estraggo l'intero contenuto dei PDF
text1 = ""
text2 = ""
for i in range(number_of_pages1):
    text1 += reader.pages[i].extract_text()

for i in range(number_of_pages2):
    text2 += reader2.pages[i].extract_text()

# Variabile booleana per determinare se le parole chiave e le diverse
# informazioni vanno recuperate dal form oppure dal matching con il 
# vocabolario giuridico
all_info = True

# Tokenizzo le intere sentenze
words1 = nltk.word_tokenize(text1, language="italian")
words2 = nltk.word_tokenize(text2, language="italian")

# Rimuovo i segni di punteggiatura dai token
words1 = [ word for word in words1 if word not in string.punctuation ]
words2 = [ word for word in words2 if word not in string.punctuation ]

# Creo i bigrammi all'interno del mio documento, poichè il dizionario contiene
# definizioni comprendenti più parole
dim1 = len(words1)
dim2 = len(words2)

# Estraggo i bigrammi dalla lista di parole 
if dim1 % 2 == 0:
    bigrams1 = []
    for i in range(0, len(words1), 2):
        bigrams1.append(words1[i] + " " + words1[i+1])
else:
    bigrams1 = []
    for i in range(0, len(words1)-1, 2):
        bigrams1.append(words1[i] + " " + words1[i+1])
    bigrams1.append(words1[len(words1)-1])

if dim2 % 2 == 0:
    bigrams2 = []
    for i in range(0, len(words2), 2):
        bigrams2.append(words2[i] + " " + words2[i+1])
else:
    bigrams2 = []
    for i in range(0, len(words2)-1, 2):
        bigrams2.append(words2[i] + " " + words2[i+1])
    bigrams2.append(words2[len(words2)-1])

# Recupero le definizioni dal vocabolario giuridico
vocabulary = []

with open("dizionariogiuridico/output.txt", "r") as f:
    vocabulary.extend(f.readlines())

# Ulteriore filtraggio per rimuovere i '\n'
vocabulary = [ element.strip() for element in vocabulary ]

# Ordino la lista di parole
words1.sort()
words2.sort()

i = 0
j = 0

'''
    Semplice algoritmo che scorre in parallelo le due liste ordinate alfabeticamente
    e sposta i puntatori in entrambe le liste in base all'ordinamento alfabetico 
    tra la parola corrente in lista1 e la parola corrente in lista2.
    Costo: O(m+n)
'''
keywords1 = []
while (i != len(words1) and j != len(vocabulary)):
    if words1[i] in vocabulary[j]:
        keywords1.append(words1[i])

    if (words1[i] > vocabulary[j]):
        j = j+1
    elif (words1[i] <= vocabulary[j]):
        i = i+1

i = 0
j = 0

# Idem per la seconda sentenza
keywords2 = []
while (i != len(words2) and j != len(vocabulary)):
    if words2[i] in vocabulary[j]:
        keywords2.append(words2[i])

    if (words2[i] > vocabulary[j]):
        j = j+1
    elif (words2[i] <= vocabulary[j]):
        i = i+1

# Rimuovo i duplicati
keywords1 = list(set(keywords1))
keywords2 = list(set(keywords2))

# Rimuovo le eventuali stopwords
keywords1 = [element for element in keywords1 if element not in italian_stopwords]
keywords2 = [element for element in keywords2 if element not in italian_stopwords]

print(keywords1)
print(keywords2)

# Stesso procedimento per i bigrammi: ordinamento e matching con il vocabolario
bigrams1.sort()
bigrams2.sort()

i = 0
j = 0

bigrams_keywords1 = []
while (i != len(bigrams1) and j != len(vocabulary)):
    if bigrams1[i] in vocabulary[j]:
        bigrams_keywords1.append(bigrams1[i])

    if (bigrams1[i] > vocabulary[j]):
        j = j+1
    elif (bigrams1[i] <= vocabulary[j]):
        i = i+1

i = 0
j = 0

bigrams_keywords2 = []
while (i != len(bigrams2) and j != len(vocabulary)):
    if bigrams2[i] in vocabulary[j]:
        bigrams_keywords2.append(bigrams2[i])

    if (bigrams2[i] > vocabulary[j]):
        j = j+1
    elif (bigrams2[i] <= vocabulary[j]):
        i = i+1

# Rimozione duplicati e rimozione stopwords
bigrams_keywords1 = list(set(bigrams_keywords1))
bigrams_keywords2 = list(set(bigrams_keywords2))

bigrams_keywords1 = [element for element in bigrams_keywords1 if element not in italian_stopwords]
bigrams_keywords2 = [element for element in bigrams_keywords2 if element not in italian_stopwords]

print(bigrams_keywords1)
print(bigrams_keywords2)

# Creazione dei documenti da inserire poi in ElasticSearch aggiungendo il campo parole chiave
doc1 = {
    'author': '1',
    'info': text1,
    'creationdate': reader.documentInfo["/CreationDate"],
    'moddate': reader.documentInfo["/ModDate"],
    'keywords': keywords1
}

doc2 = {
    'author': '2',
    'info': text2,
    'creationdate': reader2.documentInfo["/CreationDate"],
    'moddate': reader2.documentInfo["/ModDate"],
    'keywords': keywords2
}