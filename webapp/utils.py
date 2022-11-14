from flask import request
import numpy as np
import re

def striphtml(data):
    p = re.compile(r'<.*?>')
    data = p.sub(' ', data)
    data = data.replace('\n', '')
    return data

def extract_info(id, df):
    dic = {}
    dic["Numero Sentenza"] = df.iloc[id, 0]
    dic["Data Pubblicazione Sentenza"] = df.iloc[id, 1]
    dic["Registro Generale"] = df.iloc[id, 2]
    index = df.columns.get_loc("Riferimenti Normativi")
    for i in range(3, index):
        dic[df.columns[i]] = df.iloc[id, i]
    
    dic["Riferimenti Normativi"] = df.iloc[id, index]
    dic["Precedenti"] = df.iloc[id, index+1]
    dic["Giudice"] = df.iloc[id, index+2]
    dic["Parole chiave"] = df.iloc[id, index+3]
    dic["Motivazione"] = df.iloc[id, index+4]

    for key,val in dic.items():
        if str(val) == 'nan':
            dic[key] = ""

    return dic

def build_options_dict():
    options_dict = {
        "ns": "Numero Sentenza",
        # "d": "Data",
        "rg": "Registro Generale",
        "c": "Categorie Semplici",
        "o": "Oggetti",
        "rn": "Riferimenti Normativi",
        "p": "Precedenti",
        "keywords": "Parole chiave"
    }

    return options_dict


def get_fields(form):
    input_termine = form["cercatermine"]
    input_numerosentenza = form["numerosentenza"]
    # input_d = form["data-box"]
    input_rg = form["rg"]
    # input_c = form["categorie-semplici-box"]
    # input_o = form["oggetti-box"]
    # input_choice_rn = form["riferimenti"]
    input_riferimenti = form["riferimenti"]
    input_precedenti = form["precedenti"]
    input_keywords = form["parolechiave"]
    input_giudice = form["giudice"]
    
    return {
        "termine": input_termine,
        "ns": input_numerosentenza,
        # "d": input_d,
        "rg": input_rg,
        # "c": input_c,
        # "o": input_o,
        # "choice_rn": input_choice_rn,
        "rn": input_riferimenti,
        "p": input_precedenti,
        "keywords": input_keywords,
        "giu": input_giudice
    }


def execute_simple_query(input_query, client, INDEX_NAME):

    query_body = {
        "bool": {
            "should": {
                'query_string': {
                    'query': input_query
                }
            }
        }   
    }

    highlight = {
        "fields": {
            "Testo sentenza": { "type": "plain" }
        }
    }

    res = client.search(index=INDEX_NAME, query=query_body, highlight=highlight)
    # print(res)

    return res


def execute_complex_query(search_data, client, INDEX_NAME):

    query_body = {
        "bool": {
            "should": [
                {
                    "term": {
                        "Testo sentenza": search_data["termine"]
                    }
                },
                {
                    "term": {
                        "Numero Sentenza": search_data["ns"]
                    }
                },
                {
                    "term": {
                        "Registro Generale": search_data["rg"]
                    }
                },
                {
                    "term": {
                        "Riferimenti Normativi": search_data["rn"]
                    }
                },
                {
                    "term": {
                        "Precedenti": search_data["p"]
                    }
                },
                {
                    "term": {
                        "Parole chiave": search_data["keywords"]
                    }
                },
                {
                    "term": {
                        "Giudice": search_data["giu"]
                    }
                },
            ]
        }   
    }

    highlight = {
        "fields": {
            "Testo sentenza": { "type": "plain" }
        }
    }

    res = client.search(index=INDEX_NAME, query=query_body, highlight=highlight)
    # print(res)

    return res