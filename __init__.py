from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")


@app.route('/commit/')
def commit():
    try:
        # Appeler l'API GitHub pour récupérer les commits
        response = urlopen('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))

        # Construire une liste avec les informations nécessaires
        results = []
        for commit in json_content:
            commit_value = commit.get('sha')  # Identifiant du commit
            author_value = commit.get('commit', {}).get('author', {}).get('name')  # Nom de l'auteur
            date_value = commit.get('commit', {}).get('author', {}).get('date')  # Date du commit

            if commit_value and author_value and date_value:
                results.append({
                    'commit': commit_value,
                    'auteur': author_value,
                    'date': date_value
                })

        return jsonify(results=results)
    except Exception as e:
        # Gestion des erreurs en cas de problème avec l'API ou autre
        return jsonify(error=str(e)), 500


  
if __name__ == "__main__":
  app.run(debug=True)
  #commentaire
