from flask import Flask, render_template, jsonify
import pandas as pd
import requests
import io
import json

# Création d'une application Flask
app = Flask(__name__)

# Prendre en compte les modifications de template
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

# Adresse générant les données nécessaires pour le sunburst
@app.route('/sunburstdata')
def get_sunburst_data():
    # URL du fichier Excel contenant les données
    excel_url = 'https://cloud.lycee-experimental.org/s/LMw46oacXzBgXLw/download/D%C3%A9penses.xlsx'
    
    # Télécharger le fichier Excel en utilisant la bibliothèque requests
    response = requests.get(excel_url)
    
    # Lire le contenu du fichier Excel avec Pandas
    df = pd.read_excel(io.BytesIO(response.content))
    
    # Séparer une colonne en plusieurs colonnes en utilisant des espaces comme séparateurs
    df[['tmp', 'Service', 'Catégorie']] = df['CGR A'].str.split().values.tolist()

    # Regrouper les données en utilisant plusieurs colonnes comme clés
    grouped = df.groupby(["Service", "Catégorie","Libellé compte","Nom du fournisseur / élève","Libellé 1"])

    # Créer une structure de données pour le sunburst
    structure = {
        "name": "",
        "children": []
    }
    
    # Parcourir les groupes de données
    for (l1, l2, l3, l4, l5), group in grouped:
        # Rechercher le nœud l1 dans la structure
        l1_node = next((node for node in structure["children"] if node["name"] == l1), None)
        if l1_node is None:
            # Si le nœud l1 n'existe pas, le créer
            l1_node = {
                "name": l1,
                "children": []
            }
            structure["children"].append(l1_node)

        # Rechercher le nœud l2 dans le nœud l1
        l2_node = next((node for node in l1_node["children"] if node["name"] == l2), None)
        if l2_node is None:
            # Si le nœud l2 n'existe pas, le créer
            l2_node = {
                "name": l2,
                "children": []
            }
            l1_node["children"].append(l2_node)

        # Rechercher le nœud l3 dans le nœud l2
        l3_node = next((node for node in l2_node["children"] if node["name"] == l3), None)
        if l3_node is None:
            # Si le nœud l3 n'existe pas, le créer
            l3_node = {
                "name": l3,
                "children": []
            }
            l2_node["children"].append(l3_node)

        # Rechercher le nœud l4 dans le nœud l3
        l4_node = next((node for node in l3_node["children"] if node["name"] == l4), None)
        if l4_node is None:
            # Si le nœud l4 n'existe pas, le créer
            l4_node = {
                "name": l4,
                "children": []
            }
            l3_node["children"].append(l4_node)

        # Créer le nœud l5 et l'ajouter au nœud l4
        l5_node = {
            "name": l5,
            "date": group['Date comptable facture'].values[0],
            "value": group["Prix réceptionné TTC"].values[0]
        }
        l4_node["children"].append(l5_node)
    
    # Renvoyer la structure de données au format JSON
    return jsonify(structure)

# Adresse générant les données depuis un fichier excel.
@app.route('/data')
def get_data():
    # URL du fichier Excel sur le web
    excel_url = 'https://cloud.lycee-experimental.org/s/Hy6fCi6D5CZAWgd/download/D%C3%A9penses.xlsx'
    
    # Télécharger le fichier Excel en utilisant la bibliothèque requests
    response = requests.get(excel_url)
    
    # Lire le contenu du fichier Excel avec Pandas
    df = pd.read_excel(io.BytesIO(response.content), sheet_name='Donnees')
    
    # Convertir les données en format JSON
    json_data = df.to_json(orient='records')
    
    # Renvoyer les données au format JSON
    return jsonify(json.loads(json_data))

# Lancement de l'application Flask
if __name__ == '__main__':
    app.run()
