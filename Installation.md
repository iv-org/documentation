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

Compiling invidious requires at least 2GB of free RAM (We recommend to have at least 3GB installed).
If you have less (e.g on a cheap VPS) you can setup a SWAP file or partition, so the combined amount is >= 3GB.

After installation take a look at the [Post-install steps](#post-install-configuration).

Note: Any [PaaS](https://en.wikipedia.org/wiki/Platform_as_a_service) or [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service) provider/software (Heroku, YunoHost, Repli...) are unsupported, use them at your own risk, they **WILL** cause problems with Invidious. If you use one and want to report an issue, please mention which one you use.

---

## Automated installation

[Invidious-Updater](https://github.com/tmiland/Invidious-Updater) is a self-contained script that can automatically install and update Invidious.

---

## Docker

> The Invidious docker image is only [available on Quay](https://quay.io/repository/invidious/invidious) because, unlike Docker Hub, [Quay is Free and Open Source Software](https://github.com/quay/quay/blob/master/LICENSE). This is reflected in the `docker-compose.yml` file used in this walk-through.{.is-warning}

Ensure [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) are installed before beginning.

### Docker-compose method (production)

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
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER $$POSTGRES_DB"]
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
      INVIDIOUS_CONFIG: | # Follow the config/config.yml file from the main repository to know the available configuration options
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

Note: This compose is made for a true "production" setup, where Invidious is behind a reverse proxy. If you prefer to directly access Invidious, replace `127.0.0.1:3000:3000` with `3000:3000` under the `ports:` section.

> The environment variable `POSTGRES_USER` cannot be changed. The SQL config files that run the initial database migrations are hard-coded with the username `kemal`.
{.is-warning}


### Docker-compose method (development)

```bash
$ git clone https://github.com/iv-org/invidious.git
$ cd invidious
$ docker-compose up
```

---

## Manual installation

### Linux

#### Install crystal

Follow the instructions for your distribution here: https://crystal-lang.org/install/

#### Install the dependencies

Arch Linux
```bash
$ sudo pacman -S base-devel librsvg postgresql
```

Ubuntu or Debian
```bash
$ sudo apt install libssl-dev libxml2-dev libyaml-dev libgmp-dev libreadline-dev postgresql librsvg2-bin libsqlite3-dev zlib1g-dev libpcre3-dev libevent-dev
```

Fedora
```bash
$ sudo dnf install -y openssl-devel libevent-devel libxml2-devel libyaml-devel gmp-devel readline-devel postgresql librsvg2-devel sqlite-devel zlib-devel gcc
```

#### Add an Invidious user and clone the repository

```bash
$ useradd -m invidious
$ su - invidious
$ git clone https://github.com/iv-org/invidious
$ exit
```

#### Set up PostgresSQL

```bash
$ systemctl enable --now postgresql
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
$ su - invidious
$ cd invidious
$ shards build src/invidious.cr --release
$ exit
```

#### Systemd service

```bash
$ cp /home/invidious/invidious/invidious.service /etc/systemd/system/invidious.service
$ systemctl enable --now invidious.service
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
$ shards build src/invidious.cr --release
```

## Post-install configuration:

Detailed configuration available in the [configuration guide](./Configuration.md).

Because of various issues Invidious **must** be restarted often, at least once a day, ideally every hours.

If you use a reverse proxy, you **must** configure invidious to properly serve request through it:

`https_only: true` : if your are serving your instance via https, set it to true

`domain: domain.ext`: if you are serving your instance via a domain name, set it here

`external_port: 443`: if your are serving your instance via https, set it to 443

## Update Invidious

#### Updating a Docker install
```bash
$ docker-compose pull && docker-compose up && docker image prune -f
```

#### Update a manual install
```bash
$ sudo - invidious
$ cd invidious
$ currentVersion=$(git rev-list --max-count=1 --abbrev-commit HEAD)
$ git pull
$ for i in `git rev-list --reverse --abbrev-commit $currentVersion..HEAD` ; do file=./config/migrate-scripts/migrate-db-$i.sh ; [ -f $file ] && $file ; done
$ shards build src/invidious.cr --release
$ exit
$ systemctl restart invidious.service
```

## Usage:

```bash
$ ./invidious
```


#### Logrotate configuration

```bash
$ echo "/home/invidious/invidious/invidious.log {
rotate 4
weekly
notifempty
missingok
compress
minsize 1048576
}" | tee /etc/logrotate.d/invidious.logrotate
$ chmod 0644 /etc/logrotate.d/invidious.logrotate
```
