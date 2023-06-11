from flask import Flask, render_template, jsonify
import pandas as pd
import requests
import io
import json

# Création d'une application Flask'
app = Flask(__name__)

# Prendre en compte les modifications de template
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Page d'accueil'
@app.route('/')
def index():
    return render_template('index.html')

# Page affichant un camembert'
@app.route('/camembert')
def camembert():
    return render_template('camembert.html')

# Page affichant un sunburst
@app.route('/sunburst')
def sunburst():
    return render_template('sunburst.html')

# Adresse générant les données nécessaires pour le sunburst
@app.route('/sunburstdata')
def get_sunburst_data():
    # Read the contents of the JSON file
    with open('flare-2.json', 'r') as file:
        data = json.load(file)
    # Return the JSON data
    return jsonify(data)


# Adresse génrant les données depuis un fichier excel.
@app.route('/data')
def get_data():
    # URL du fichier Excel sur le web
    excel_url = 'https://cloud.lycee-experimental.org/s/Hy6fCi6D5CZAWgd/download/D%C3%A9penses.xlsx'
    
    # Télécharger le fichier Excel en utilisant requests
    response = requests.get(excel_url)
    
    # Lire le contenu du fichier Excel avec Pandas
    df = pd.read_excel(io.BytesIO(response.content), sheet_name='Donnees')
    
    # Convertir les données en format JSON
    json_data = df.to_json(orient='records')
    
    # Renvoyer les données au format JSON
    return jsonify(json.loads(json_data))

# Lancement de Flask
if __name__ == '__main__':
    app.run()

