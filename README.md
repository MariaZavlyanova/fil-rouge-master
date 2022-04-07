# Fil rouge

Thématique globale du projet: Transformation automatisée de la donnée en connaissance. 
Objectifs pédagogiques :  


Objectifs du projet : 
Le projet consiste à établir un graphe de connaissances (une sorte de « google scholar »)  
des auteur, des documents produits, avec qui, en citant qui, extraits de toutes les 
publications en « Computer Science & AI » du site ArXiv.org. Le graphe de connaissances 
ainsi construit devra permettre de répondre à des interrogations comme « qui influence 
qui  ? » (interrogation en SPARQL), voire même à l'aide de règles (SWRL) d'établir de 
nouvelles relations entre les auteurs (Bonus). 
Ce projet peut être synthétisé en première approche comme un pipe-line de traitements à 
trois modules : EXTRACTION, TLA, ONTO 



Livrables : 
• L'ensemble du projet est à remettre sur Edunao (des précisions suivront) au plus tard le 
vendredi 8 avril 2022 à 23h59 ; 
• Le projet est individuel : chacun remet l'intégralité des livrables sous son nom, par contre 
les travaux, notamment de réflexion peuvent se faire en groupe ; 
• Le livrable est une archive comprimée au format zip qui comprend : 
        1. Un rapport technique sur l'ensemble de l'architecture, qui explique les choix et justifie 
les performances du modèle (question de la diapo 4), la description de l'API qui permet 
d'accéder au module TLA, un exemple d'interrogation avec le langage SPARQL, quelques 
mots d'explications sur les éventuelles règles SWRL écrites et les déductions de nouvelles 
relations trouvées (BONUS). 25 pages maximum. 
        2. Le source Python commenté de l'ensemble du « pipe-line » de traitement (hors module 
TLA), sous forme d'un Notebook (Jupyter vs JupyterLab) ; 
        3. Le source Python du module « as a service » (diapo 4) constituant externe du « pipe-line » ; 
        4. Un fichier au format XML (par exemple sortie de l'outil Protégé) avec l'ontologie FOAF chargée, des individus et relations ajoutées.

# Install

## Dependencies

This package requires python 3 (including venv), git and a recent Ubuntu OS


## Usage

Clone and go to the newly created repository :

    $ git clone https://gitlab-student.centralesupelec.fr/maria.zavlyanova/fil-rouge.git

Create a virtualenv and activate it: (here our venv is called "filerougevenv")

    $ python3 -m venv .venv
    $ source .venv/bin/activate

Install requirements from txt file:

    $ pip install -r requirements.txt


## Create json dataset

Cette partie a déjà été initialisée, il faudrai supprimer le fichier avant de vouloir recommencer, si non il y aura des doublons

    $ cd code/app/init_data/
    $ python dataset.py
    # changer le nomre d'articles qui seront extraits dans le code

# Access to the dataset via API

Lancer l'API

    $ cd code/app/
    $ uvicorn main:app --reload

open http://127.0.0.1:8000 in a browser

# API specification

### Upload and extract metadata from id of PDF

You only need the id of the pdf:

**Request**

    HTTP Methode: GET
    Route: /extract_metadata/<pdf_id>
    # Replace <id> by ID of the chosen document
    # The ID is the id of the URL

Example :

for the URL : http://arxiv.org/pdf/2202.01645v1

the API method is : http://127.0.0.1:8000/extract_metadata/2202.01645v1

### Extract Metadata from an uploaded metadata

Get the metadata that we already have:

**Request**

    HTTP Methode: GET
    Route: /metadata/<pdf_id>
    # Replace <id> by ID of the chosen document
    # The ID is the id of the URL

Example :

for the URL : http://arxiv.org/pdf/2202.01645v1

the API method is : http://127.0.0.1:8000/metadata/2202.01645v1

# OpenApi method

    http://127.0.0.1:8000/redoc

# FastAPI in Containers - Docker
## Build the Docker Image

    $ docker build -t myimage .

## Start the Docker Container

    $ docker run -d --name mycontainer -p 80:80 myimage

## Check it :

You should be able to check it in your Docker container's URL, 

for example: http://192.168.99.100/items/5?q=somequery or http://127.0.0.1/items/5?q=somequery (or equivalent, using your Docker host).

You will see something like:

        {"item_id": 5, "q": "somequery"}


## OWL
- Auteur (a écrit un article)

        - Auteur cité (a écrit un article, cité par un auteur) sous classe de Auteur

                - Inluenceur (a été cité par au moins 10 auteur) sous classe de auteur cité

                - Auteur de niche (a été cité par un Auteur maximum)

- Article (ecrit par un auteur) - a une année

        - Article cité (cité par un auteur) sous classe de article

                - Article important (INDEX DE CITATION supérieur à 10 (échelle de ma BDD)) sous classe de article cité
                
                - Article de niche (a été cité par un Auteur maximum)
