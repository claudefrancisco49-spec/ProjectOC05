db = db.getSiblingDB('hpcare_db');

db.createUser({
  user: "user_h",
  pwd: "apph1234",
  roles: [
    {
      role: "readWrite",
      db: "hpcare_db"
    }
  ]
});

