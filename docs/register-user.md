# Registering users manually
You might want to disable registration in your [instance config](/configuration), but still have a quick way to manually register users upon request. To do so, first set up a separate instance that only listens on localhost, has registration enabled,
and captchas as well as background jobs disabled. Make sure you have a way to start it easily with just one or a few commands, e.g. via a systemd service. Then, use something like the script below (in the example, the instance is started via a systemd
service called `podman-invidious_register`, and it listens on localhost port 21742. **Warning**: This script is vulnerable to SQL injections. Only use trusted inputs; if you want to make a custom signup form and use this as a backend, be sure to
sanitize inputs.
```sh
#!/usr/bin/env bash
set -e

systemctl start podman-invidious_register

CONTINUE='y'
while [ "$CONTINUE" = 'y' ]; do
    read -rp 'User ID: ' ID
    if [ "$(su postgres -c "psql invidious -c \"SELECT email FROM users WHERE email = '\"'$ID'\"';\"" | tail -n 2 | head -n 1)" != '(0 rows)' ]; then
        echo 'Error: User ID is already taken'
        continue
    fi

    read -rsp 'Password: ' PASSWORD

    curl -L 'http://localhost:21742/login' --form-string "email=$ID" --form-string "password=$PASSWORD" -F 'action=signin' >/dev/null

    read -rp 'Register more accounts? [y/N] ' CONTINUE
done

systemctl stop podman-invidious_register
```
