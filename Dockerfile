# On s'appuie sur l'image python:3.14-slim
# On se base sur une image à taille réduite, ici
FROM python:3.14-slim
# Notre répertoire de travail /appmdb
# sera à la racine du système de fichier
# du conteneur
WORKDIR /appmdb
# On créait le répertoire data projet
RUN mkdir -p /data 
# On copy les data projet du host vers le répertoire projet
COPY /data/*.csv ./data/
# On copy les script python du host vers le répertoire projet
COPY /app/*.py .
COPY /app/run.sh .
COPY /test/*.py .
# On copy le fichier des dépendances projet du host vers le répertoire projet
COPY requirements.txt .
# On installe les dépendances de notre application  pandas pymongo ...
RUN pip install --no-cache-dir -r requirements.txt
# Rendre le fichier run.sh executable par le conteneur
RUN chmod +x run.sh 
# Définition de notre commande par défaut
# => Lancer run.sh (Ordonnanceur *.py dans le conteneur) 
CMD ["/bin/bash","run.sh"]
#CMD ["/bin/sh"]
# Définition d'une étiquette arbitraire sur notre image
LABEL description="Un conteneur pour charger la data csv dans mongodb."
