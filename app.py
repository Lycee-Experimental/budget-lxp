from flask import Flask, render_template, jsonify, request
import pandas as pd
import requests
import io
import json
from utils import *

# Création d'une application Flask
app = Flask(__name__)

# Activation du rechargement automatique des templates
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html', title='Accueil')

# Page affichant un camembert
@app.route('/camembert')
def camembert():
    return render_template('camembert.html')

# Page affichant un sunburst
@app.route('/sunburst')
def sunburst():    
    if request.args.get("budget_previ"):
        title='Budget prévisionnel'
    else:
        title='Budget'
    return render_template('sunburst.html', title=title)

@app.route('/stackbar')
def stackbar():    
    return render_template('stackbars.html', title='Jauge des dépenses')


# Route générant les données nécessaires pour le sunburst
@app.route('/data')
def data():
    # Si la demande est d'afficher le budget prévisionnel
    if request.args.get("budget_previ"):
        traduction_budget_previ(budget_previ)
        return jsonify(budget_previ)
    # Sinon, on récupère les éventuelles dates de débuts et de fin
    else :
        debut=request.args.get("debut") if request.args.get("debut") else None
        fin=request.args.get("fin") if request.args.get("fin") else None
        return get_data(debut, fin)

# Route générant les données à partir d'un fichier Excel
@app.route('/data2')
def get_data2():
    # URL du fichier Excel sur le web
    excel_url = 'https://cloud.lycee-experimental.org/s/Hy6fCi6D5CZAWgd/download/D%C3%A9penses.xlsx'
    
    # Téléchargement du fichier Excel en utilisant requests
    response = requests.get(excel_url)
    
    # Lecture du contenu du fichier Excel avec Pandas
    df = pd.read_excel(io.BytesIO(response.content), sheet_name='Donnees')
    
    # Remplacement des valeurs NaN par une chaîne vide
    df.fillna('', inplace=True)
    
    # Conversion des données en format JSON
    json_data = df.to_json(orient='records')
    
    # Renvoi des données au format JSON
    return jsonify(json.loads(json_data))

# Lancement de Flask
if __name__ == '__main__':
    app.run()
