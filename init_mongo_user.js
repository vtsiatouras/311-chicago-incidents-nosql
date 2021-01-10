db.createUser(
    {
        user: "test_user",
        pwd: "password",
        roles:[
            {
                role: "readWrite",
                db:   "mydatabase"
            }
        ]
    }
);
