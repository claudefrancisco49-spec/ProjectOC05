db = db.getSiblingDB('hcare_db');

db.createUser({
  user: "user_h",
  pwd: "apph1234",
  roles: [
    {
      role: "readWrite",
      db: "hcare_db"
    }
  ]
});

