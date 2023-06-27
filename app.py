from flask import Flask, render_template, jsonify, request
import pandas as pd
import requests
import io
import json

# Création d'une application Flask
app = Flask(__name__)

# Activation du rechargement automatique des templates
app.config['TEMPLATES_AUTO_RELOAD'] = True

budget_previ = {   'name': '',
    'children' : [{  'name': 'FONCT',
                    'children' : [  {   'name': '0LEXPASS',
                                        'value' : 2000
                                    },
                                    {   'name': '0LEXPCARB',
                                        'value' : 1000
                                    },
                                    {   'name': '0LEXPCONT',
                                        'value' : 6500
                                    },
                                    {   'name': '0LEXPENT',
                                        'value' : 3400
                                    },
                                    {   'name': '0LEXPEQ',
                                        'value' : 3000
                                    },
                                    {   'name': '0LEXPFOUR',
                                        'value' : 3000
                                    },
                                    {   'name': '0LEXPHYG',
                                        'value' : 4000
                                    },
                                    {   'name': '0LEXPLOC',
                                        'value' : 116000
                                    },
                                    {   'name': '0LEXPPTT',
                                        'value' : 3500
                                    },
                                    {   'name': '0LEXPREC',
                                        'value' : 1500
                                    },
                                    {   'name': '0LEXPVEHI',
                                        'value' : 2000
                                    },
                                    {   'name': '0LEXPVIAB',
                                        'value' : 16000
                                    }
                                ]
                 },
                 {  'name': 'ENS',
                    'children' : [  {   'name': '0LEXART',
                                        'value' : 2000
                                    },
                                    {   'name': '0LEXDOCUM',
                                        'value' : 2200
                                    },
                                    {   'name': '0LEXPEDAG',
                                        'value' : 7100
                                    },
                                    {   'name': '0LEXSORTI',
                                        'value' : 4800
                                    },
                                    {   'name': '2 CEA XP',
                                        'value' : 5000
                                    },
                                    {   'name': '13REPLEXP',
                                        'value' : 220
                                    }
                                ]
                }
        ]
}

traduction = {
                'ENS': 'Pédagogie',
                'FONCT': 'Fonctionnement',
                '0LEXART': 'Dépenses artistiques',
                '0LEXDOCUM': 'Documentation',
                '0LEXPEDAG': 'Dépenses pédagogiques',
                '0LEXSORTI': 'Sorties et voyages',
                '0LEXPASS': 'Assurances',
                '0LEXPCARB': 'Carburant',
                '0LEXPCONT': 'Contrats maintenance',
                '0LEXPENT': 'Entretien/réparation',
                '0LEXPEQ': 'Petit équipement',
                '0LEXPFOUR': 'Fournitures',
                '0LEXPHYG': 'Hygiène',
                '0LEXPLOC': 'Locations',
                '0LEXPPTT': "Poste & télécom'",
                '0LEXPREC': 'Frais de réception',
                '0LEXPVEHI': 'Entretien vehicule',
                '0LEXPVIAB': 'Viabilisation',
                '13REPLEXP': 'Reprographie',
                '2 CEA XP' : 'CEA (Région)',
                '040ALXP' : "Com' externe",
                'REPAS' : 'Repas',
                '0LEXPMO' : 'Nourriture',
                'TRAVAU' : 'Travaux',
                '0LEXPTVX' : 'Travaux',
                'FOURNITURES NON STOCKABLES - GAZ' : 'Gaz',
                'FOURNITURES NON STOCKABLES - ELECTRICITE' : 'Electricité',
                'FOURNITURES NON STOCKABLES - EAU' : 'Eau',
                'AUTRES FOURNITURES (MAT. MOB. OUTIL. NON IMMOBILISABLES)' : 'Autres fournitures',
                'FOURNITURES ADMINISTRATIVES' : 'Fournitures admin',
                'FOURNITURES NON STOCKABLES - CARBURANTS ET LUBRIFIANTS' : 'Carburants et lubrifiants',
                'VOYAGES DEPL. MISSIONS ELEVES & ETUDIANTS - VOYAGES' : 'Voyages',
                'VOYAGES DEPL. MISSIONS ELEVES & ETUDIANTS - SORTIES' : 'Sorties',
                'LIVRES PEDAG. & ADMIN. (NON DEMAT.) OUVRAGES CDI' : 'Livres',
                "FOURNITURES ET MATERIELS D'ENSEIGNEMENT (NON IMMOBILISABLES)" : 'Fournitures',
                'PERSONNELS EXTERIEURS A L’ETABLISSEMENT' : 'Intervenants',
                'LINGE, VETEMENTS DE TRAVAIL ET PRODUITS DE NETTOYAGE' : 'Hygiène',
                'FRAIS DE RECEPTIONS (PRESTATIONS EXTERIEURES)' : 'Frais de réception',
                'FRAIS POSTAUX ET FRAIS DE TELECOMMUNICATIONS' : 'Poste & Télécom',
                'SOUS TRAITANCE - DIVERSES PRESTATIONS D’ENTRETIEN' : "Entretiens",
                'AUTRES ACTIVITES SOUS-TRAITEES' : 'Maintenances',
                'Carburants et lubrifiants': 'Diesel',
                'AUTRES LOCATIONS' : 'Autres locations',
                'BRICOLAND': 'Leroy Merlin',
                'DISMER': 'Promocash',
                'CASTORAMA OCEANIS': 'Castorama',
                'CSF': 'Carrefour',
                'SIDERIS OUEST': 'Sidéris',
                'SOCULTUR': 'Cultura',
                'ENGIE ENERGIE SERVICES': 'Engie',
                'LES HAMEAUX BIO': 'Biocop',
                'BOULANGER': 'Boulanger',
                'LOCATIONS IMMOBILIERES': 'Loyer',
                "OFFICE PUBLIC DE L'HABITAT SILENE": 'Silène',
                'OFFICE DEPOT ST NAZAIRE': 'Office Dépot',
                'PUBLICITE, PUBLICATIONS, RELATIONS PUBLIQUES': 'Pub',
                'INFIRMERIE ET PRODUITS PHARMACEUTIQUES': 'Pharma',
                "FOURNITURES ET PETIT MATERIEL D'ENTRETIEN": 'Fournitures entretien'            
}

def traduction_budget_previ(budget_previ):
    # Mise à jour de la propriété name du nœud racine
    budget_previ['name'] = traduction[budget_previ['name']] if budget_previ['name'] in traduction else budget_previ['name']
    # Mise à jour récursive des propriétés name des nœuds enfants
    if 'children' in budget_previ:
        for child in budget_previ['children']:
            traduction_budget_previ(child) if child['name'] in traduction else traduction_budget_previ(child)

def is_date_between(date, start_date, end_date):
    date = pd.to_datetime(date, format="%d/%m/%Y")
    start_date = pd.to_datetime(start_date, format="%d/%m/%Y") if start_date else None
    end_date = pd.to_datetime(end_date, format="%d/%m/%Y") if end_date else None
    # Vérification si la date est comprise entre les dates de début et de fin
    return (not start_date or start_date <= date) and (not end_date or date <= end_date)



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
@app.route('/data')
def get_sunburst_data():
    # Si la demande est d'afficher le budget prévisionnel
    if request.args.get("budget_previ"):
        traduction_budget_previ(budget_previ)
        return jsonify(budget_previ)
    # Sinon, on récupère les éventuelles dates de débuts et de fin
    debut=request.args.get("debut") if request.args.get("debut") else None
    fin=request.args.get("fin") if request.args.get("fin") else None

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
    df2['Date comptable facture'] = df2['Date comptable facture'].dt.strftime("%d/%m/%Y")
    # Fusion des deux DataFrames    
    merged_df = pd.concat([df, df2])
    # Remplacement des valeurs NaN par une chaîne vide
    merged_df.fillna('', inplace=True)

    # Création de la structure pour le sunburst
    structure = create_node('')

    
    def fonct_traduction(cle):
        if cle in traduction:
            return traduction[cle]
        else:
            return cle

    # Parcours des lignes du DataFrame
    for _, row in merged_df.iterrows():
        # Vérification si la date est comprise entre les dates de début et de fin
        if not is_date_between(row['Date comptable facture'], debut, fin):
            continue
        # Récupération des valeurs des colonnes
        domaine = fonct_traduction(row['Domaine'])
        activite = fonct_traduction(row['Activité'])
        libelle_compte = fonct_traduction(row['Libellé compte'].strip())
        fournisseur = fonct_traduction(row['Nom du fournisseur / élève'].strip())
        libelle = row['Libellé 1'].strip()
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
@app.route('/data2')
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
