from flask import Flask, render_template, jsonify, request
from utils import *


# Création d'une application Flask
app = Flask(__name__)

# Activation du rechargement automatique des templates
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html', title='Accueil')

# Page affichant un sunburst
@app.route('/budget/sunburst')
def sunburst():    
    if request.args.get("budget_previ"):
        title='Budget prévisionnel'
    else:
        title='Budget'
    return render_template('sunburst.html', title=title)

@app.route('/budget/stackbar')
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
        return get_data(data,debut, fin)

# Lancement de Flask
if __name__ == '__main__':
    data = load_data()
    app.run()
