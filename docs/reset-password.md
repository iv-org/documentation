# Reset user password

Resetting a user's Invidious password needs you to edit the database.

Firstly, generate a bcrypt-encrypted hash for the new password you want to set for the user.

This can, for example, be done with the `bcrypt` python module or the `mkpasswd` shell utility (the latter should be preinstalled on most systems):

```
python3 -c 'import bcrypt; print(bcrypt.hashpw(b"<INSERT PASSWORD HERE>", bcrypt.gensalt(rounds=10)).decode("ascii"))' # python
mkpasswd --method=bcrypt-a -R 10 # mkpasswd
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

This script bundles all needed commands so you don't have to enter everything manually every time, and also checks that the username exists before writing to the database:
```sh
#!/bin/sh
set -e

printf 'User ID: '
read -r ID
if [ "$(su postgres -c "psql invidious -c \"SELECT email FROM users WHERE email = '$ID';\"" | tail -n 2 | head -n 1)" != '(1 row)' ]; then
    echo 'Error: User ID does not exist'
    exit 1
fi

HASH="$(mkpasswd --method=bcrypt-a -R 10)"
su postgres -c "psql invidious -c \"UPDATE users SET password = '\"'$HASH'\"' WHERE email = '\"'$ID'\"';\""
```
