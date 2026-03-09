# On s'appuie sur l'image python:3.11-slim
# On se base sur une image à taille réduite, ici
FROM python:3.14-slim
# Notre répertoire de travail
# sera la racine du système de fichier
# du conteneur
WORKDIR /appmdb
# On créait le répertoire projet /...
RUN mkdir -p /data 
COPY /data/*.csv ./data/
COPY /app/*.py .
COPY /app/run.sh .
COPY /test/*.py .
COPY requirements.txt .
# On installe les dépendances de notre application
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install pandas pymongo
# On créait l’utilisateur “myuser” avec des droits standards
RUN adduser --system myuser
RUN chown -R myuser /appmdb && chmod +x run.sh 
# On bascule sur l’utilisateur “myuser”
# USER myuser
# Définition de notre commande par défaut
# => Lancer *.py dans le conteneur 
CMD ["/bin/sh","run.sh"]
#CMD ["/bin/sh"]
# Définition de notre commande par défaut
# Définition d'une étiquette arbitraire sur notre image
LABEL description="Un conteneur pour charger la data csv dans mongodb."
