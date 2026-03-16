# On s'appuie sur l'image mongo:7
FROM mongo:7
# Script d'initialisation pour créer un utilisateur applicatif
COPY init-user.js ./docker-entrypoint-initdb.d/
# Création d'un compte utilisateur user_h des datas hopital uniquement
# Rendre le fichier init-user.js executable par le conteneur
RUN cd ./docker-entrypoint-initdb.d/ && chmod 644 init-user.js

