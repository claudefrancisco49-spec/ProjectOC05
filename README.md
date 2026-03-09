# Migration des données vers MongoDB via Docker 
- Script python afin d’automatiser la migration du dataset healthcare_dataset.csv reçu vers MongoDB.
- Docker pour conteneuriser MongoDB ainsi que le(s) script(s) de migration des données afin que le tout soit portable et scalable.

## Arborescence répertoire projet migration mongodb

migration_mongodb/ \
│── Dockerfile \
│── docker-compose.yml \
│── requirements.txt \
│── README.MD \
│ \
├── app/ \
│   │── main.py \
│   │── read_csv.py \
│ \
├── test/ \
│   │── test_csv.py \
│   │── test_mongodb.py \
│ \
└── data/ healthcare_dataset.csv

## Démarrer docker-compose

1. Se positionner dans le répertoire:

   ```/bin/sh
   cd home/misc/migration_mongodb
   ```

2. Exécuter la commande `docker compose build`

Après quelques secondes, l'image des conteneurs docker-compose devrait être prêt.

3. Exécuter la commande `docker compose up`

Après quelques secondes, les conteneurs docker-compose devraient être initialisés et prêts à l'emplois (autotest et migration csv -> mongodb terminer).

## Manipuler appmdb (débug script python)

1. Se positionner dans le répertoire projet du host et modifier le Dockerfile avec la commande suivante:

CMD ["/bin/sh"]

1. Se positionner dans le répertoire projet du host:

ubuntu@ubuntu2204:~/misc/migration_mongodb$ sudo docker build -t pyapp:latest .

2. Exécuter la commande
ubuntu@ubuntu2204:~/misc/migration_mongodb$ sudo docker run -v $(pwd)/data:/appmdb/data -it --rm --name test pyapp:latest

3. Vous ête dans le conteneur, tapez:

$ ls -la
