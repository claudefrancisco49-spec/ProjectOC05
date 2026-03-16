# Migration des données vers MongoDB via Docker 

- Script python afin d’automatiser la migration du dataset healthcare_dataset.csv reçu vers MongoDB.
- Docker pour conteneuriser MongoDB ainsi que le(s) script(s) de migration des données afin que le tout soit portable et scalable.

## Arborescence projet migration mongodb

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

`CMD ["/bin/sh"]`

2. Se positionner dans le répertoire projet du host et exécuter la commande `docker build`:

ubuntu@ubuntu2204:~/misc/migration_mongodb$ sudo docker build -t pyapp:latest .

3. Exécuter la commande `docker run`
ubuntu@ubuntu2204:~/misc/migration_mongodb$ sudo docker run -v $(pwd)/data:/appmdb/data -it --rm --name test pyapp:latest

4. Vous ête dans le conteneur, tapez:

$ ls -la

## Manipuler mongodb (débug et test script python)

### Test de sécurité (sans autentification)

1. Se positionner dans le répertoire projet du host et exécuter la commande `docker compose up`

ubuntu@ubuntu2204:~/misc/migration_mongodb$ sudo docker compose up

2. Exécuter la commande `docker compose exec -it mongo bash`

3. Vous êtes dans le conteneur mongo, tapez:

$ mongosh

4. Mongosh prompt, tapez:

test> use admin
admin> show databases
ou
admin> show users
MongoServerError[Unauthorized]: Command usersInfo requires authentication

admin>exit

### Testez l'autentification admin

1. Se positionner dans le répertoire projet du host et exécuter la commande `docker compose exec -it mongo mongosh` avec autentification:

ubuntu@ubuntu2204:~/misc/migration_mongodb$ sudo docker compose exec -it mongo mongosh -u admin_hp -p pass1234 --authenticationDatabase admin

2. Vous êtes dans le conteneur mongo, tapez:
test> use hcare_db
switched to db hcare_db

3. Vous êtes dans le conteneur mongo database hcare_db, tapez:

hcare_db> show collections
hospital

hcare_db> use admin
admin> show users
[
  {
    _id: 'admin.admin_hp',
    userId: UUID('f8671fcc-3b57-41c9-9681-d1cb4ab3abd1'),
    user: 'admin_hp',
    db: 'admin',
    roles: [ { role: 'root', db: 'admin' } ],
    mechanisms: [ 'SCRAM-SHA-1', 'SCRAM-SHA-256' ]
  }
]

### Testez l'autentification user

1. Se positionner dans le répertoire projet du host et exécuter la commande `docker compose exec -it mongo mongosh` avec autentification:

ubuntu@ubuntu2204:~/misc/migration_mongodb$ sudo docker compose exec -it mongo mongosh -u user_h -p apph1234 --authenticationDatabase hcare_db

2. Vous êtes dans le conteneur mongo et la seul database accessible est hcare_db, tapez:

test> use admin
switched to db admin
admin> show databases
hcare_db  8.00 MiB

3. Vous êtes dans le conteneur mongo database pcare_db et souhaitez consulter le nom d'un patient sans les droits admin, tapez:

admin> db.getUsers()
MongoServerError[Unauthorized]: not authorized on admin to execute command { usersInfo: 1, lsid: { id: UUID("2e85d7b1-9a38-41c0-8ef0-a2c0eb3187b0") }, $db: "admin" }

admin> use pcare_db
switched to db pcare_db
pcare_db> show collections
MongoServerError[Unauthorized]: not authorized on pcare_db to execute command { listCollections: 1, filter: {}, cursor: {}, nameOnly: true, authorizedCollections: false, lsid: { id: UUID("4aa3eac3-b4c2-4518-9c72-181f3eeb9d54") }, $db: "pcare_db" }

### Arrêtez les conteneurs

1. Vous êtes dans le conteneur mongo et souhaitez arrêter le conteneur , tapez:

ubuntu@ubuntu2204:~/misc/migration_mongodb$ sudo docker compose down -v
[+] down 5/5
 ✔ Container migration_mongodb-mongo-express-1 Removed                                                                                                                              1.5s
 ✔ Container migration_db                      Removed                                                                                                                              1.4s
 ✔ Container mongo                             Removed                                                                                                                              0.4s
 ✔ Network migration_mongodb_app-network       Removed                                                                                                                              0.1s
 ✔ Network migration_mongodb_client-network    Removed                                                                                                                              0.2s

2. A faire : Ne pas oublier de nettoyer la data si vous vouler rexécuter le script python, tapez:

ubuntu@ubuntu2204:~/misc/migration_mongodb$ sudo rm -rf data
ubuntu@ubuntu2204:~/misc/migration_mongodb$ mkdir data
ubuntu@ubuntu2204:~/misc/migration_mongodb$ cp healthcare_dataset.csv data/
ubuntu@ubuntu2204:~/misc/migration_mongodb$ ls data/
healthcare_dataset.csv

