# Mortpion

Prérequis : 

- installer le serveur `bdw-server`
- installer `Mortpion` (jeu de données, configuration config-bd.toml, déplacement du répertoire)
- lancer Mortpion :
```sh
# activer l'environnement virtuel (déjà créé) dans bdw-server/
source .venv/bin/activate  # ou .venv\Scripts\activate sous windows
# lancer le serveur avec le paramètre DIRECTORY qui contient votre site web
python server.py Mortpion
# si tout est ok, aller sur http://localhost:4242/ (URL par défaut)
```


