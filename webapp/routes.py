from flask import current_app as app
from flask import render_template
from flask import request
from flask import send_from_directory, send_file
import os
from utils import *
from wsgi import client, INDEX_NAME

@app.route('/')
def home():

    return render_template(
        'home.html',
        title="Ivstitia Search!"
    )


@app.route('/guida', methods=["GET"])
def guida():
    return render_template(
        'guida.html'
    )

@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        input_query = request.form["search-box"]
        print(input_query)
        return render_template(
            'search.html'
        )

@app.route('/accessibility')
def accessibility():
    return render_template(
        'accessibility.html'
    )

@app.route('/insert')
def insert():
    return render_template(
        'insert.html'
    )


@app.route('/advanced-search', methods=["GET"])
def advancedsearch():
    options_dict = build_options_dict()

    return render_template(
        'advanced_search.html',
        options_dict = options_dict
    )



@app.route('/results', methods=["GET", "POST"])
def results():
    if request.method == "POST":
        simple = False
        try:
            request.form["numerosentenza"]
        except:
            simple = True

        # If simple is true then the request is simple
        if simple:
            input_query = request.form["Barra di Ricerca"]
            print(input_query)
            # Execute query on ElasticSearch
            res = execute_simple_query(input_query, client, INDEX_NAME)
        else:
            search_data = get_fields(request.form)

            print(search_data)
            # Execute query on ElasticSearch 
            res = execute_complex_query(search_data, client, INDEX_NAME)

        highlights = []
        # Build the snippet
        for j,sentenza in enumerate(res["hits"]['hits']):
            highlight = ""
            try:
                sentenza["highlight"]
                for i in range(len(sentenza["highlight"]["Testo sentenza"])):
                    if i != len(sentenza["highlight"]["Testo sentenza"]):
                        highlight += (striphtml(sentenza["highlight"]["Testo sentenza"][i])).strip()
                        highlight += " ... "
                    else:
                        highlight += (striphtml(sentenza["highlight"]["Testo sentenza"][i])).strip()

                highlights.append(highlight.strip())

                res["hits"]["hits"][j]["highlight"]["Formatted"] = highlight.strip()
            except KeyError:
                pass
            


            
        print(res["hits"]["hits"])

        '''
            In both cases, we collect the Json results from ElasticSearch and we 
            convert it in a suitable python format. Then we will pass these objects
            to the below render_template and use Jinja2 to display things dynamically
        '''
        return render_template(
            "results.html",
            res = res["hits"]['hits']
        )


@app.route('/results/<int:id>')
def act(id):

    hit = client.get(index=INDEX_NAME, id=id)

    return render_template(
        "act.html",
        hit = hit
    )


# @app.get("/download/<path:filename>")
@app.route('/<path:filename>', methods=["GET", "POST"])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    print(uploads)
    # uploads = os.path.join(uploads, filename)
    # return send_file(os.path.join(uploads, filename), as_attachment=True)
    return send_from_directory(directory=uploads, path=filename, mimetype='application/pdf')