set -e

mongo <<EOF
use admin

db.createUser({
  user: '$MONGO_USER',
  pwd:  '$MONGO_PASSWORD',
  roles: [{
    role: 'readWrite',
    db: '$MONGO_DB'
  }]
})
EOF