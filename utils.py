import pandas as pd
import requests
import io
from flask import jsonify

budget_previ = {'name': '',
                'children': [{'name': 'FONCT',
                              'children': [{'name': '0LEXPASS',
                                            'value': 2000
                                            },
                                           {'name': '0LEXPCARB',
                                            'value': 1000
                                            },
                                           {'name': '0LEXPCONT',
                                            'value': 6500
                                            },
                                           {'name': '0LEXPENT',
                                            'value': 3400
                                            },
                                           {'name': '0LEXPEQ',
                                            'value': 3000
                                            },
                                           {'name': '0LEXPFOUR',
                                            'value': 3000
                                            },
                                           {'name': '0LEXPHYG',
                                            'value': 4000
                                            },
                                           {'name': '0LEXPLOC',
                                            'value': 116000
                                            },
                                           {'name': '0LEXPPTT',
                                            'value': 3500
                                            },
                                           {'name': '0LEXPREC',
                                            'value': 1500
                                            },
                                           {'name': '0LEXPVEHI',
                                            'value': 2000
                                            },
                                           {'name': '0LEXPVIAB',
                                            'value': 16000
                                            }
                                           ]
                              },
                             {'name': 'ENS',
                              'children': [{'name': '0LEXART',
                                            'value': 2000
                                            },
                                           {'name': '0LEXDOCUM',
                                            'value': 2200
                                            },
                                           {'name': '0LEXPEDAG',
                                            'value': 7100
                                            },
                                           {'name': '0LEXSORTI',
                                            'value': 4800
                                            },
                                           {'name': '2 CEA XP',
                                            'value': 5000
                                            },
                                            #{'name': '13EAC',
                                            # 'value': 3000
                                            #},
                                           {'name': '13REPLEXP',
                                            'value': 220
                                            }
                                           ]
                              },
                             #{'name': 'Repas', 
                             # 'children':[{'name': '0LEXPMO', 'value': 5000}],
                             #},
                             #{'name': 'Travaux', 'value': 80000}
                             ]
                }

traduction_fournisseur = {'0002641440': 'MARJORIE LE BERRE', '0002592392': "LIBRAIRIE L'EMBARCADERE", '0002583210': 'CRAP CAHIERS PEDAGOGIQUES', '0002593018': 'F&S', '0002587571': 'SOCIETE OUEST FRANCE', '0002658872': "INSTITUT COOPERATIF DE L'ECOLE MODERNE", '0002594854': 'BEAUX ARTS & CIE', '0002594537': 'CSF', '0002597753': 'LES HAMEAUX BIO', '0002597672': 'CYLIAH CREATIONS', '0002547600': 'BOULANGER', '0002650685': 'ARCANE INDUSTRIES', '0002655716': 'ANTHONY GORICHON', '0002658846': 'BERNIE COLLEAUX', '0002658826': 'PLANETE SCIENCES', '0002662592': 'BASTIEN MUSSET', '0002583222': 'SOCULTUR', '0002672123': 'AMANDINE LABBE', '0002672114': "ANIM'ENVIE", '0002598013': 'SODIF MINI-FOUINE', '0002582758': 'BRICOLAND', '0002678854': 'LAETITIA ZOBEL', '0002688600': 'COMMUNE DE LA ROCHE BERNARD', '0002919273': 'Bernadette COLLEAUX', '0002918987': 'AUCHAN HYPERMARCHE', '0002892946': 'LE PLANNING FAMILIAL 44', '0002655096': 'EMMAUS 44 - SAINT-NAZAIRE - FONDATEUR ABBE PIERRE', '0002586016': 'LE THEATRE',
                           '0002678998': 'PIERRE BRISSEAU', '0002688536': 'ESCAPADES VERTICALES', '0002689509': "ALEX'LOISIRS", '0002587342': 'MUTUELLE ASSURANCE INSTITUTEUR FRANCE', '0002592099': 'TOTALENERGIES PROXI NORD OUEST', '0002597727': 'ORONA OUEST NORD', '0002594963': 'SIDERIS OUEST', '0002550323': '3 PROTECTION', '0002594907': 'LA TRICYCLERIE SAINT-NAZAIRE', '0002582996': 'CHUBB FRANCE', '0002592905': 'ENGIE ENERGIE SERVICES', '0002594911': 'LERAY MENUISERIE', '0002587591': 'OVH', '0002582818': 'BUREAU VALLEE', '0002590060': 'TIRVIT', '0002587797': 'DISMER', '0002590213': "UNION DES GROUPEMENTS D'ACHATS PUBLICS", '0002627453': 'SYLVIENNE CARRIO', '0002582934': 'CHAMPENOIS COLLECTIVITES', '0002598195': 'PHARMACIE PAJOTIN', '0002592197': 'FRANFINANCE LOCATION', '0002588483': 'OFFICE PUBLIC DE L HABITAT SILENE', '0002585206': 'LA POSTE', '0002597495': 'ORANGE', '0002672148': 'ORANGE', '0003255663': "TONY'S SELF GARAGE", '0002641207': "COMMUNAUTE D'AGGLO DE LA REGION NAZAIRIENNE ET DE L'ESTUAIRE", '0002577435': 'ENGIE'}

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
                '2 CEA XP': 'CEA (Région)',
                '2CEAXP': 'CEA (Région)',
                '040ALXP': "Com' externe",
                'REPAS': 'Repas',
                '0LEXPMO': 'Nourriture',
                'TRAVAU': 'Travaux',
                '0LEXPTVX': 'Travaux',
                '13EAC': "Pass'Culture",
                'FOURNITURES NON STOCKABLES - GAZ': 'Gaz',
                'FOURNITURES NON STOCKABLES - ELECTRICITE': 'Electricité',
                'FOURNITURES NON STOCKABLES - EAU': 'Eau',
                'AUTRES FOURNITURES (MAT. MOB. OUTIL. NON IMMOBILISABLES)': 'Autres fournitures',
                'FOURNITURES ADMINISTRATIVES': 'Fournitures admin',
                'FOURNITURES NON STOCKABLES - CARBURANTS ET LUBRIFIANTS': 'Carburants et lubrifiants',
                'VOYAGES DEPL. MISSIONS  ELEVES & ETUDIANTS - VOYAGES': 'Voyages',
                'VOYAGES DEPL. MISSIONS  ELEVES & ETUDIANTS - SORTIES': 'Sorties',
                'LIVRES PEDAG. & ADMIN. (NON DEMAT.) OUVRAGES CDI': 'Livres',
                "FOURNITURES ET MATERIELS D'ENSEIGNEMENT (NON IMMOBILISABLES)": 'Fournitures',
                'PERSONNELS EXTERIEURS A L’ETABLISSEMENT': 'Intervenants',
                'LINGE, VETEMENTS DE TRAVAIL ET PRODUITS DE NETTOYAGE': 'Hygiène',
                'FRAIS DE RECEPTIONS (PRESTATIONS EXTERIEURES)': 'Frais de réception',
                'FRAIS POSTAUX ET FRAIS DE TELECOMMUNICATIONS': 'Poste & Télécom',
                'SOUS TRAITANCE - DIVERSES PRESTATIONS D’ENTRETIEN': "Entretiens",
                'AUTRES ACTIVITES SOUS-TRAITEES': 'Maintenances',
                'Carburants et lubrifiants': 'Diesel',
                'AUTRES LOCATIONS': 'Autres locations',
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
                'EMMAUS 44 - SAINT-NAZAIRE - FONDATEUR ABBE PIERRE': 'Emmaüs',
                "FOURNITURES ET PETIT MATERIEL D'ENTRETIEN": 'Fournitures entretien',
                "AUCHAN HYPERMARCHE": 'Auchan',
                "AFB SOCIAL AND GREENIT": "AFB",
                "UNION DES GROUPEMENTS D'ACHATS PUBLICS": "UGAP",
                "OFFICE PUBLIC DE L HABITAT SILENE": "Silène",
                "FRANFINANCE LOCATION":"FranFinance",
                "LA POSTE": "La Poste",
                "COMMUNAUTE D'AGGLO DE LA REGION NAZAIRIENNE ET DE L'ESTUAIRE": "Carène",
                "ENGIE": "Engie",
                "3 PROTECTION SOCIETE GENERALE": "3 Protection",
                "LERAY MENUISERIE": "Menuisier Leray",
                "CHUBB FRANCE": "Chubb",
                "ORONA OUEST NORD": "Orona",
                "REDEVANCES DE CREDIT-BAIL": "Location imprimantes",
                "LA TRICYCLERIE SAINT-NAZAIRE": "Tricyclerie",
                "CARENE ST NAZAIRE AGGLOMERAT°":"Carène",
                "BUREAU VALLEE":"Bureau Valée",
                "CYLIAH CREATIONS": "Cyliah Creations",
                "POP'ART DESIGN": "Pop'art design",
                "TIRVIT": "Tirvit",
                "OFFICE PUBLIC DE L HABITAT  SILENE": "Silène",
}


def traduction_budget_previ(budget_previ):
    # Mise à jour de la propriété name du nœud racine
    budget_previ['name'] = traduction[budget_previ['name']
                                      ] if budget_previ['name'] in traduction else budget_previ['name']
    # Mise à jour récursive des propriétés name des nœuds enfants
    if 'children' in budget_previ:
        for child in budget_previ['children']:
            traduction_budget_previ(
                child) if child['name'] in traduction else traduction_budget_previ(child)


def is_date_between(date, start_date, end_date):
    date = pd.to_datetime(date, format="%d/%m/%Y")
    start_date = pd.to_datetime(
        start_date, format="%d/%m/%Y") if start_date else None
    end_date = pd.to_datetime(
        end_date, format="%d/%m/%Y") if end_date else None
    # Vérification si la date est comprise entre les dates de début et de fin
    return (not start_date or start_date <= date) and (not end_date or date <= end_date)

# Fonction pour créer un noeud de la structure de donnée


def create_node(name):
    return {
        "name": name,
        "children": []
    }


def fonct_traduction(cle, dico=traduction):
    return dico.get(cle, cle.title())



def load_data():
    """Charge les données depuis le cloud"""
    # URL des fichiers Excel contenant les données
    excel_url = 'https://cloud.lycee-experimental.org/s/LMw46oacXzBgXLw/download/D%C3%A9penses.xlsx'
    excel_2022_url = 'https://cloud.lycee-experimental.org/s/aq4ZSABm2GS2eNL/download/D%C3%A9penses2022.xlsx'

    # Téléchargement des fichiers Excel en utilisant requests
    response = requests.get(excel_url)
    response_2022 = requests.get(excel_2022_url)

    # Lecture du contenu des fichiers Excel avec Pandas
    df = pd.read_excel(io.BytesIO(response.content), dtype={'Fournisseur': str})


    df2 = pd.read_excel(io.BytesIO(response_2022.content))

    # Création des colonne Domaine et Categorie à partir de "CGR A"
    df[['tmp', 'Domaine', 'Activité']] = df['CGR A'].str.split().values.tolist()
    df2['Date comptable facture'] = df2['Date comptable facture'].dt.strftime(
        "%d/%m/%Y")
    # Fusion des deux DataFrames
    merged_df = pd.concat([df, df2])
    # Remplacement des valeurs NaN par une chaîne vide
    merged_df.fillna('', inplace=True)
    # Création de la structure pour le sunburst
    merged_df = merged_df[~((merged_df['Domaine'] == 'REPAS') | (merged_df['Domaine'] == 'TRAVAU') | (merged_df['Activité'] == '13EAC'))]
    return merged_df


def get_data(df, debut, fin):
    
    structure = create_node('')

    # Parcours des lignes du DataFrame
    for _, row in df.iterrows():
        # Vérification si la date est comprise entre les dates de début et de fin
        if not is_date_between(row['Date comptable facture'], debut, fin):
            continue
        # Récupération des valeurs des colonnes
        domaine = fonct_traduction(row['Domaine'])
        activite = fonct_traduction(row['Activité'])
        libelle_compte = fonct_traduction(row['Libellé compte'].strip()).title() 
        fournisseur = fonct_traduction(row['Fournisseur'], traduction_fournisseur) if (row['Nom du fournisseur / élève'] == 0) else row['Nom du fournisseur / élève']
        fournisseur = fonct_traduction(fournisseur.strip())


        libelle = row['Libellé 1'].strip()
        date = row['Date comptable facture']
        value = row['Prix réceptionné TTC']

        # Parcours des niveaux de la structure
        current_node = structure
        for level in [domaine, activite, libelle_compte, fournisseur]:
            # Vérification si le noeud existe déjà, sinon création
            node = next(
                (n for n in current_node['children'] if n['name'] == level), None)
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
