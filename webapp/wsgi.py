from math import isnan
from init import init_app
from elasticsearch import Elasticsearch
import fitz
import os
import pandas as pd
from utils import extract_info

# Apro una connessione al daemon di ElasticSearch, restituendo il client connesso
def connect_elasticsearch(INDEX_USER, INDEX_PASS):
    _es = None
    # Put https in local, http on the remote machine
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


# Initializzo nome utente, password e nome dell'index
INDEX_USER = "elastic"
INDEX_PASS = "IipmNDcssS4IfbrjdiMy"
INDEX_NAME = "test"

# Apro la connessione
client = connect_elasticsearch(INDEX_USER, INDEX_PASS)
print(client)

# Creo un mapping per specificare che ho bisogno di un analyzer italiano per il testo del PDF
mapping = {
    "properties": {
        "Testo sentenza": {
            "type": "text",
            "analyzer": "italian"
        },
        "Motivazione": {
            "type": "text",
            "analyzer": "italian" 
        }
    }
}

try:
    # Creo l'index passando il client e il mapping
    client = index_create(INDEX_NAME, client, mapping)
except:
    print("ElasticSearch daemon is not live")

def add_docs(client, INDEX_NAME):
    df = pd.read_csv("csv_db/Modulo Inserimento Sentenze .csv")

    print(df)

    # Drop all unuseful columns
    df = df.drop(df.columns[[0, 1, 2]], axis=1)
    df = df.drop(df.columns[-7:-1], axis=1)
    df = df.drop(df.columns[-1], axis=1)

    temp = df.iloc[0].copy()
    second = df.iloc[1]
    df.iloc[0] = second
    df.iloc[1] = temp

    for id, file in enumerate(os.listdir("docs/")):

        doc = fitz.open(os.path.join("docs/", file))

        # heuristic for rectangle
        rect = fitz.Rect(0, 70.0, doc[0].rect.width - 20.0, doc[0].rect.height - 60.0)  # define your rectangle here

        text = ""
        for page in doc:
            extracted_text = ' '.join(page.get_textbox(rect).split())  # get text from rectangle
            text += extracted_text
            text += " "

        text = text.strip()

        # Variabile booleana per determinare se le parole chiave e le diverse
        # informazioni vanno recuperate dal form oppure dal matching con il 
        # vocabolario giuridico
        all_info = True

        dict_info = extract_info(id, df)            


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
            
            doc = {
                "Testo sentenza": text,
                "Path file": file
            }

            doc.update(dict_info)

            # print(doc)

        else:
            # Se all_info è false recupero le parole chiave dallo script matching_doc_voc.py
            # (va convertito in funzione per chiamarlo qui dentro)
            doc = {
                "Testo sentenza": text,
                "Path file": file
            }
            
            # Da sostituire con il recupero "automatico" delle parole chiave
            doc.update(dict_info)

        resp = client.index(index=INDEX_NAME, id=id, document=doc)
        print(resp['result'])

try:
    add_docs(client, INDEX_NAME)
except Exception as e:
    print(e)
    print("Client not live, ElasticSearch daemon is off")

app = init_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')