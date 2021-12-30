---
title: Installation
description: 
published: true
date: 2021-05-23T16:58:48.374Z
tags: 
editor: markdown
dateCreated: 2021-02-25T11:24:06.655Z
---

# Installation

Compiling Invidious requires at least 2GB of free RAM (We recommend to have at least 3GB installed).
If you have less (e.g on a cheap VPS) you can setup a swap file or partition, so the combined amount is >= 3GB.

After installation take a look at the [Post-install steps](#post-install-configuration).

### Note on blocking bots

Allowing bots that excessively crawl (Semrush, webmeup, etc.) will lead your instance to get blocked very fast. While not required, it is a good idea to consider using bot blocking software such as [Nginx Bad Bot Blocker](https://github.com/mitchellkrogza/nginx-ultimate-bad-bot-blocker).

## Automated installation

[Invidious-Updater](https://github.com/tmiland/Invidious-Updater) is a self-contained script that can automatically install and update Invidious.

## Docker

> The Invidious docker image is only [available on Quay](https://quay.io/repository/invidious/invidious) because, unlike Docker Hub, [Quay is open source](https://github.com/quay/quay/blob/master/LICENSE). This is reflected in the `docker-compose.yml` file used in this walkthrough.

Ensure [Docker Engine](https://docs.docker.com/engine/install) and [Docker Compose](https://docs.docker.com/compose/install) are installed before beginning.

### Make directory

```bash
$ mkdir invidious
```

### Create Docker Compose file

```bash
$ cd invidious
```

```bash
$ nano docker-compose.yml
```

Here is a working Compose setup:
```docker
version: "2.4"
services:
  postgres:
    image: postgres:10
    restart: always
    networks:
      - invidious
    volumes:
      - postgresdata:/var/lib/postgresql/data
      - ./config/sql:/config/sql
      - ./docker/init-invidious-db.sh:/docker-entrypoint-initdb.d/init-invidious-db.sh
    environment:
      POSTGRES_DB: invidious
      POSTGRES_USER: kemal
      POSTGRES_PASSWORD: kemal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]
  invidious:
    image: quay.io/invidious/invidious:latest
    restart: always
    networks:
      - invidious
    mem_limit: 1024M
    cpus: 0.5
    ports:
      - "127.0.0.1:3000:3000"
    environment:
      INVIDIOUS_CONFIG: |
        channel_threads: 1
        check_tables: true
        feed_threads: 1
        db:
          dbname: invidious
          user: kemal
          password: kemal
          host: postgres
          port: 5432
        full_refresh: false
        https_only: false
        domain:
      # external_port:
    healthcheck:
      test: wget -nv --tries=1 --spider http://127.0.0.1:3000/api/v1/comments/jNQXAC9IVRw || exit 1
      interval: 30s
      timeout: 5s
      retries: 2
    depends_on:
      - postgres
  autoheal:
    restart: always
    image: willfarrell/autoheal
    environment:
      - AUTOHEAL_CONTAINER_LABEL=all
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

volumes:
  postgresdata:

networks:
  invidious:
```

> The environment variable `POSTGRES_USER` cannot be changed. The SQL config files that run the initial database migrations are hard-coded with the username `kemal`.

### Start Invidious

```bash
$ docker-compose up
```
or
```bash
$ docker-compose up -d
```
to run it in the background.

Then, visit `localhost:3000` in your browser.

### Stop Invidious

```bash
$ docker-compose down
```

### Delete data

```bash
$ docker volume rm invidious_postgresdata
```

## Manual Installation

### Linux

#### Install Crystal

Follow the instructions for your distribution [here](https://crystal-lang.org/install)

If you're in a hurry, here are one-liner commands for some common distributions:
* Arch Linux `sudo pacman -S crystal shards`
* Debian/Ubuntu: `curl -fsSL https://crystal-lang.org/install.sh | sudo bash`
* Fedora: `sudo brew update && sudo brew install crystal-lang`

Or you can do a tarball install:
```bash
cd ~/Downloads
wget https://github.com/crystal-lang/crystal/releases/download/1.1.1/crystal-1.1.1-1-linux-x86_64.tar.gz
cd /opt
sudo tar -xzf ~/Downloads/crystal-1.1.1-1-linux-x86_64.tar.gz
sudo cp /opt/crystal-1.1.1-1/bin/{crystal,shards} /usr/local/bin/
sudo cp -r /opt/crystal-1.1.1-1/lib/crystal /usr/local/lib/crystal
sudo cp -r /opt/crystal-1.1.1-1/share/crystal /usr/local/share/crystal
```

#### Install the dependencies

Arch Linux
```bash
sudo pacman -S base-devel librsvg postgresql
```

Debian/Ubuntu
```bash
sudo apt-get update
sudo apt install libssl-dev libxml2-dev libyaml-dev libgmp-dev libreadline-dev postgresql librsvg2-bin libsqlite3-dev zlib1g-dev libpcre3-dev libevent-dev
```

Fedora
```bash
sudo dnf install -y openssl-devel libevent-devel libxml2-devel libyaml-devel gmp-devel readline-devel postgresql librsvg2-devel sqlite-devel zlib-devel gcc
```

#### Add an Invidious user and clone the repository

```bash
$ useradd -m invidious
$ sudo -i -u invidious
$ git clone https://github.com/iv-org/invidious
$ exit
```

#### Set up PostgresSQL

```bash
$ sudo systemctl enable --now postgresql
$ sudo -i -u postgres
$ psql -c "CREATE USER kemal WITH PASSWORD 'kemal';" # Change 'kemal' here to a stronger password, and update `password` in config/config.yml
$ createdb -O kemal invidious
$ psql invidious kemal < /home/invidious/invidious/config/sql/channels.sql
$ psql invidious kemal < /home/invidious/invidious/config/sql/videos.sql
$ psql invidious kemal < /home/invidious/invidious/config/sql/channel_videos.sql
$ psql invidious kemal < /home/invidious/invidious/config/sql/users.sql
$ psql invidious kemal < /home/invidious/invidious/config/sql/session_ids.sql
$ psql invidious kemal < /home/invidious/invidious/config/sql/nonces.sql
$ psql invidious kemal < /home/invidious/invidious/config/sql/annotations.sql
$ psql invidious kemal < /home/invidious/invidious/config/sql/playlists.sql
$ psql invidious kemal < /home/invidious/invidious/config/sql/playlist_videos.sql
$ exit
```

#### Set up Invidious

```bash
$ sudo -i -u invidious
$ cd invidious
$ shards update && shards install
$ crystal build src/invidious.cr --release
# test compiled binary
$ ./invidious # stop with ctrl c
$ exit
```

#### Systemd service

```bash
$ sudo cp /home/invidious/invidious/invidious.service /etc/systemd/system/invidious.service
$ sudo systemctl enable --now invidious.service
```

#### Logrotate

```bash
$ echo "/home/invidious/invidious/invidious.log {
rotate 4
weekly
notifempty
missingok
compress
minsize 1048576
}" | sudo tee /etc/logrotate.d/invidious.logrotate
$ sudo chmod 0644 /etc/logrotate.d/invidious.logrotate
```

### MacOS

```bash
# Install dependencies
$ brew update
$ brew install shards crystal postgres imagemagick librsvg

# Clone the repository and set up a PostgreSQL database
$ git clone https://github.com/iv-org/invidious
$ cd invidious
$ brew services start postgresql
$ psql -c "CREATE ROLE kemal WITH PASSWORD 'kemal';" # Change 'kemal' here to a stronger password, and update `password` in config/config.yml
$ createdb -O kemal invidious
$ psql invidious kemal < config/sql/channels.sql
$ psql invidious kemal < config/sql/videos.sql
$ psql invidious kemal < config/sql/channel_videos.sql
$ psql invidious kemal < config/sql/users.sql
$ psql invidious kemal < config/sql/session_ids.sql
$ psql invidious kemal < config/sql/nonces.sql
$ psql invidious kemal < config/sql/annotations.sql
$ psql invidious kemal < config/sql/privacy.sql
$ psql invidious kemal < config/sql/playlists.sql
$ psql invidious kemal < config/sql/playlist_videos.sql

# Set up Invidious
$ shards update && shards install
$ crystal build src/invidious.cr --release
```

## Post-install configuration:

Detailed configuration available in the [configuration guide](./Configuration.md).

Because of various issues, Invidious **must** be restarted often, at least once a day, ideally every  <!--TODO: add the number of hours--> hours.

If you use a reverse proxy, you **must** configure invidious to properly serve request through it:

`https_only: true` : if you are serving your instance via https, set it to true

`domain: domain.ext`: if you are serving your instance via a domain name, set it here

`external_port: 443`: if you are serving your instance via https, set it to 443

## Update Invidious

Instructions are available in the [updating guide](./Updating.md).

## Usage:

```bash
$ ./invidious -h
Usage: invidious [arguments]
    -b HOST, --bind HOST             Host to bind (defaults to 0.0.0.0)
    -p PORT, --port PORT             Port to listen for connections (defaults to 3000)
    -s, --ssl                        Enables SSL
    --ssl-key-file FILE              SSL key file
    --ssl-cert-file FILE             SSL certificate file
    -h, --help                       Shows this help
    -c THREADS, --channel-threads=THREADS
                                     Number of threads for refreshing channels (default: 1)
    -f THREADS, --feed-threads=THREADS
                                     Number of threads for refreshing feeds (default: 1)
    -o OUTPUT, --output=OUTPUT       Redirect output (default: STDOUT)
    -v, --version                    Print version
```

Or for development:

```bash
$ curl -fsSLo- https://raw.githubusercontent.com/samueleaton/sentry/master/install.cr | crystal eval
$ ./sentry
🤖  Your SentryBot is vigilant. beep-boop...
```
