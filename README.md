# Budget-LXP

## Introduction

**Buget-LXP** est une application pour afficher des tableaux et graphiques en lien avec la comptabilité du Lycée Expérimental de Saint-Nazaire.

Cette application se base sur des données `xls` exportées via le logiciel comptable **Op@le**.

La librairie de traitement des données en table [Pandas](https://pandas.pydata.org/) permet de traiter et convertir ces données en format `json`.

Un framework Web en python, [Flask](https://flask.palletsprojects.com) est utilisé pour distribuer à la fois les fichiers json et les pages web en html sur lesquelles nous créons des graphiques.

Enfin, les graphiques sont créés grâce à la librairie [d3.js](https://d3js.org/) 

## Installation

Pour télécharger le code et installer les dépendances sur votre ordinateur équipé de linux en base Debian (Ubuntu, Mint...), lancer le code suivant dans un terminal :

```shell
cd 
sudo apt install python3-pip git
git clone https://github.com/lycee-experimental/budget-lxp
cd budget-lxp
pip install -r requirements.txt
```

## Lancement

Pour lancer l'application :

```shell
cd ~/budget-lxp
python3 app.py
```

Vous accèderez alors à l'application à l'addresse : [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Développement
- Le fichier `app.py` (Flask) permet de créer de nouvelles **pages web** ou de nouveaux traitements de **données json** (Pandas).
- Les différents fichiers `html` contenus dans le dossier templates sont ceux affichés par `app.py` (**Flask**) et contiennent les codes en javascript pour créer les graphiques **d3.js**.


## Quelques exemples d'utilisation de d3.js

- https://github.com/d3/d3/wiki/Gallery

- https://www.react-graph-gallery.com/

- https://observablehq.com/@d3/gallery

- https://observablehq.com/@d3/bar-chart-race

- https://d3-graph-gallery.com/barplot.html

