# Banca Dati
Implementazione di una banca dati giuridica per il progetto europeo PNRR

## Descrizione dettagliata
Di seguito troviamo la struttura ad albero dell'intero progetto, e a seguire una descrizione di ogni componente

```
banca_dati                                 
├─ csv_db                                  
│  └─ Modulo Inserimento Sentenze .csv
├─ dizionariogiuridico                     
│  └─ output.txt                          
├─ docs                                   
│  ├─ 39-2021 evidenziata.pdf              
│  └─ sent. 103 - 2021 v.pdf               
├─ docs2                               
│  └─ Sent 179-2021.pdf                    
├─ src                                     
│  ├─ extract_massima.py                   
│  ├─ matching_doc_voc.py                  
│  ├─ prova.py                             
│  ├─ scraping.py                          
│  └─ search_engine.py                     
├─ webapp                                  
│  ├─ static                               
│  │  ├─ able                              
│  │  │  ├─ build                          
│  │  │  │  ├─ ....     
│  │  │  ├─ button-icons                   
│  │  │  │  ├─ black                       
│  │  │  │  │  ├─ ....
│  │  │  │  ├─ fonts                       
│  │  │  │  │  ├─ ....              
│  │  │  │  ├─ white                       
│  │  │  │  │  ├─ ....    
│  │  │  │  └─ able-icons.svg              
│  │  │  ├─ images                         
│  │  │  │  └─ wingrip.png                 
│  │  │  ├─ styles                         
│  │  │  │  └─ ableplayer.css              
│  │  │  ├─ translations                   
│  │  │  │  ├─ ....                   
│  │  │  └─ LICENSE                        
│  │  ├─ audio                             
│  │  │  └─ memories.mp3                   
│  │  ├─ css                               
│  │  │  └─ style.css                      
│  │  └─ images                            
│  │     ├─ favicon.ico                    
│  │     ├─ logo_uni.png                   
│  │     └─ xicon.svg                      
│  ├─ templates                            
│  │  ├─ accessibility.html                
│  │  ├─ act.html                          
│  │  ├─ advanced_search - Copy (2).html   
│  │  ├─ advanced_search.html              
│  │  ├─ base.html                         
│  │  ├─ guida.html                        
│  │  ├─ home.html                         
│  │  ├─ insert.html                       
│  │  ├─ leftbar.html                      
│  │  └─ results.html                      
│  ├─ __init__.py                          
│  ├─ routes.py                            
│  └─ utils.py                             
├─ README.md                               
├─ config.py                               
├─ requirements.txt                        
└─ wsgi.py                                 
```

* csv_db
  - Modulo Inserimento Sentenze .csv: è il file csv che viene scaricato dal relativo form di inserimento sentenze, da cui verranno estratti i campi per popolare il documento giuridico
* dizionariogiuridico
  - output.txt: un dizionario giuridico scaricato dal sito Brocardi.it, per effettuare l'individuazione automatica delle parole chiave all'interno degli atti giuridici    
* docs: cartella contenente tutti gli atti giuridici presenti sul motore di ricerca, al momento ne sono presenti due 
* docs2: cartella alternativa contenente gli atti per il lavoro sull'evidenziazione 
* src
  - extract_massima.py: script python che estrae la "massima" dall'atto giuridico, ovvero tutte le porzioni di testo evidenziate (i giuristi caricano gli atti con solamente la massima evidenziata)
  - matching_doc_voc.py: cerca all'interno degli atti giuridici le parole (o coppie di parole) che compaiono all'interno del vocabolario output.txt
  - scraping.py: effettua il web scraping dal sito Brocardi.it andando a creare il dizionario
* webapp: contiene file statici e script per far funzionare il sito
  - static: cartella contenente diversi file statici, come immagini, file audio, fonts, css etc...
  - templates: contiene tutti i file html collegati alle diverse pagine del sito, formattati tramite il web template engine Jinja2
  - __init__.py: Lancia la webapp
  - routes.py: contiene il routing e la logica delle diverse pagine della webapp, gli endpoint raggiungibili tramite barra di ricerca e i metodi HTTP ammessi
  - utils.py: contiene diverse funzioni utilizzate nella logica della webapp, all'interno di routes.py per "snellire" il codice all'interno di quest'ultima
* config.py: contiene diverse variabili di configurazione per ElasticSearch
* requirements.txt: contiene i requirements di Python da installare 
* wsgi.py: Script da lanciare per eseguire la webapp, effettua l'avvio del motore di ricerca con il caricamento dei documenti e fa partire l'app vera e propria
