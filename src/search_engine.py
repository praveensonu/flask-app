from elasticsearch import Elasticsearch
import PyPDF2
from datetime import datetime
import os

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

# Ogni oggetto reader conterrà diverse informazioni riguardanti il PDF
print(reader.documentInfo)

# Variabile booleana per determinare se le parole chiave e le diverse
# informazioni vanno recuperate dal form oppure dal matching con il 
# vocabolario giuridico
all_info = True

''' 
    Se all_info è settato a True, allora dovrò recuperare le informazioni dal form che
    sarà stato compilato da un giurista. Quindi:
    - va aggiunto un campo ID che identifica univocamente il documento all'interno poi di ElasticSearch
      (in fase di indexing quando aggiungo un documento all'index di ElasticSearch mi viene richiesto un ID,
      tanto vale aggiungerlo anche nelle informazioni del documento stesso per tenerne traccia)
    - vanno aggiunti tutti i diversi campi che compaiono nel form, ovvero codici civili, codici penali,
      codici di procedura, giudice (coinciderà con il campo _author_) ecc..  
    - _info_ conterrà il contenuto del PDF
    - _creationdate_ and _moddate_ vengono recuperati dalle informazioni ottenute in lettura del PDF
      (data di creazione e ultima data di modifica)
'''
if all_info:
    
    doc1 = {
        'author': '1',
        'info': text1,
        'creationdate': reader.documentInfo["/CreationDate"],
        'moddate': reader.documentInfo["/ModDate"]
    }

    doc2 = {
        'author': '2',
        'info': text2,
        'creationdate': reader2.documentInfo["/CreationDate"],
        'moddate': reader2.documentInfo["/ModDate"]
    }
else:
    # Se all_info è false recupero le parole chiave dallo script matching_doc_voc.py
    # (va convertito in funzione per chiamarlo qui dentro)
    doc1 = {
        'author': '1',
        'info': text1,
        'creationdate': reader.documentInfo["/CreationDate"],
        'moddate': reader.documentInfo["/ModDate"]
    }

    doc2 = {
        'author': '2',
        'info': text2,
        'creationdate': reader2.documentInfo["/CreationDate"],
        'moddate': reader2.documentInfo["/ModDate"]
    }

# Initializzo nome utente, password e nome dell'index
INDEX_USER = "elastic"
INDEX_PASS = "IipmNDcssS4IfbrjdiMy"
INDEX_NAME = "test"

# Apro una connessione al daemon di ElasticSearch, restituendo il client connesso
def connect_elasticsearch(INDEX_USER, INDEX_PASS):
    _es = None
    _es = Elasticsearch("https://localhost:9200", basic_auth=(INDEX_USER, INDEX_PASS), ssl_show_warn=False, verify_certs=False)
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es

# Crea un indice eliminando eventualmente quello già esistente
def index_create(INDEX_NAME, client, mapping):
    if client.indices.exists(index=INDEX_NAME):
        client.indices.delete(index=INDEX_NAME)
    client.indices.create(index=INDEX_NAME, mappings=mapping)
    print("Index Created!")
    return client

# Apro la connessione
client = connect_elasticsearch(INDEX_USER, INDEX_PASS)
print(client)

# Creo un mapping per specificare che ho bisogno di un analyzer italiano per il testo del PDF
mapping = {
    "properties": {
        "info": {
            "type": "text",
            "analyzer": "italian"
        }
    }
}

# Creo l'index passando il client e il mapping
client = index_create(INDEX_NAME, client, mapping)

# Utilizzo il metodo index del client per aggiungere un documento a ElasticSearch
# Il campo id è il campo univoco che identifica il documento, e quindi come scritto sopra
# pensavo di utilizzare tipo id=doc1["ID"]
resp = client.index(index=INDEX_NAME, id=1, document=doc1)
print(resp['result'])
resp = client.index(index=INDEX_NAME, id=2, document=doc2)
print(resp['result'])

# Stampa il mapping per verificare che l'analyzer è impostato correttamente a italian
# print(client.indices.get_mapping(index=INDEX_NAME))
# resp = client.get(index=INDEX_NAME, id=1)
# print(resp['_source'])

# Refresh index: solitamente il refresh è asincrono e viene chiamato automaticamente 
# quando si effettua una search
client.indices.refresh(index=INDEX_NAME)

# Creazione di una query: cerco il termine "palmaccio" all'interno del testo delle sentenze
term = "palmaccio"

# Esempio di piccola query già complessa: ritorno tutti i documenti che devono (must) contenere 
# all'interno di info (match) il termine 'term'.
# Il termine must puo' essere sostituito da 'should' per avere risultati con più gradi di libertà
query_body = {
    "bool": {
        "must": [
            {"match": {"info": term}},
        ]
    }, 
    "highlight": {
        "fields": {
            "content": {}
        }
    }     
}

# Eseguo la query e stampo i risultati
res = client.search(index=INDEX_NAME, query=query_body)
print ("Found {} results.".format(res['hits']['total']['value']))
for hit in res['hits']['hits']:
    print ("score: {} author: {}".format(hit["_score"], hit["_source"]["author"]))
    print ("body: {}".format(hit["_source"]["info"])[:100])
