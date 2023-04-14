# How to reset a user's password

Resetting a user's invidious password needs you to edit the database.

Firstly, generate a bcrypt-encrypted hash for the new password you want to set for the user.

This can be done with the `bcrypt` python module, though there are other ways of doing the same.

```
python3 -c 'import bcrypt; print(bcrypt.hashpw(b"<INSERT PASSWORD HERE>", bcrypt.gensalt(rounds=10)).decode("ascii"))'
```

To do so, first attach to the database:
```
# su - postgres
$ psql
postgres=# \c invidious
```

Now, run the following SQL query:
```
UPDATE users SET password = 'HASH' WHERE email = 'USERNAME';
```

After that, the password should be reset.
