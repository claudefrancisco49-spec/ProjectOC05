#FROM mongo:6
#FROM mongo:3.4
#FROM mongo:latest
FROM mongo:7
# Variables d'environnement pour l'utilisateur admin
#ENV MONGO_INITDB_ROOT_USERNAME=admin_hp
#ENV MONGO_INITDB_ROOT_PASSWORD=pass1234
# Base de données par défaut
#ENV MONGO_INITDB_DATABASE=hcare_db
#COPY *.conf ./etc/
# Script d'initialisation pour créer un utilisateur applicatif
COPY init-user.js ./docker-entrypoint-initdb.d/
RUN cd ./docker-entrypoint-initdb.d/ && chmod 644 init-user.js

