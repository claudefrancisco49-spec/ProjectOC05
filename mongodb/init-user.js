db = db.getSiblingDB('hcare_db');

db.createUser({
  user: process.env.USERNAME_MDB_U,
  pwd: process.env.PASSWORD_MDB_U,
  roles: [
    {
      role: "readWrite",
      db: "hcare_db"
    }
  ]
});

