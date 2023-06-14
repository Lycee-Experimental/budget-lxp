from flask import Flask, render_template, jsonify
import pandas as pd
import requests
import io
import json

# Création d'une application Flask
app = Flask(__name__)

# Activation du rechargement automatique des templates
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Page affichant un camembert
@app.route('/camembert')
def camembert():
    return render_template('camembert.html')

# Page affichant un sunburst
@app.route('/sunburst')
def sunburst():
    return render_template('sunburst.html')

# Fonction pour créer un noeud de la structure
def create_node(name):
    return {
        "name": name,
        "children": []
    }

# Route générant les données nécessaires pour le sunburst
@app.route('/sunburstdata')
def get_sunburst_data():
    # URL des fichiers Excel contenant les données
    excel_url = 'https://cloud.lycee-experimental.org/s/LMw46oacXzBgXLw/download/D%C3%A9penses.xlsx'
    excel_2022_url = 'https://cloud.lycee-experimental.org/s/aq4ZSABm2GS2eNL/download/D%C3%A9penses2022.xlsx'
    
    # Téléchargement des fichiers Excel en utilisant requests
    response = requests.get(excel_url)
    response_2022 = requests.get(excel_2022_url)

    # Lecture du contenu des fichiers Excel avec Pandas
    df = pd.read_excel(io.BytesIO(response.content))
    df2 = pd.read_excel(io.BytesIO(response_2022.content))

    # Création des colonne Domaine et Categorie à partir de "CGR A"
    df[['tmp', 'Domaine', 'Activité']] = df['CGR A'].str.split().values.tolist()

    # Fusion des deux DataFrames    
    merged_df = pd.concat([df, df2])
    # Remplacement des valeurs NaN par une chaîne vide
    merged_df.fillna('', inplace=True)

    # Création de la structure pour le sunburst
    structure = create_node('')

    # Parcours des lignes du DataFrame
    for _, row in merged_df.iterrows():
        # Récupération des valeurs des colonnes
        domaine = row['Domaine']
        activite = row['Activité']
        libelle_compte = row['Libellé compte']
        fournisseur = row['Nom du fournisseur / élève']
        libelle = row['Libellé 1']
        date = row['Date comptable facture']
        value = row['Prix réceptionné TTC']
        
        # Parcours des niveaux de la structure
        current_node = structure
        for level in [domaine, activite, libelle_compte, fournisseur]:
            # Vérification si le noeud existe déjà, sinon création
            node = next((n for n in current_node['children'] if n['name'] == level), None)
            if not node:
                node = create_node(level)
                current_node['children'].append(node)
            current_node = node
        
        # Création du noeud pour le libellé et ajout au fournisseur_node
        leaf_node = {
            "name": libelle,
            "date": date,
            "value": value
        }
        current_node['children'].append(leaf_node)

    return jsonify(structure)


# Route générant les données à partir d'un fichier Excel
@app.route('/data')
def get_data():
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
