---
title: Installation
description: 
published: true
date: 2021-02-25T18:05:08.275Z
tags: 
editor: markdown
dateCreated: 2021-02-25T11:24:06.655Z
---

## Installation:

To manually compile invidious you need at least 2GB of RAM. If you have less you can setup SWAP to have a combined amount of 2 GB or use Docker instead.

After installation take a look at the [Post-install steps](#post-install-configuration).

### Automated installation:

[Invidious-Updater](https://github.com/tmiland/Invidious-Updater) is a self-contained script that can automatically install and update Invidious.

### Docker:

#### Build and start cluster:

```bash
$ docker-compose up
```

Then visit `localhost:3000` in your browser.

#### Rebuild cluster:

```bash
$ docker-compose build
```

#### Delete data and rebuild:

```bash
$ docker volume rm invidious_postgresdata
$ docker-compose build
```

### Manual installation:

### Linux:

#### Install the dependencies

```bash
# Arch Linux
$ sudo pacman -S base-devel shards crystal librsvg postgresql

# Ubuntu or Debian
# First you have to add the repository to your APT configuration. For easy setup just run in your command line:
$ curl -fsSL https://crystal-lang.org/install.sh | sudo bash
# That will add the signing key and the repository configuration. If you prefer to do it manually, Follow the instructions here https://crystal-lang.org/install
$ sudo apt-get update
$ sudo apt install crystal libssl-dev libxml2-dev libyaml-dev libgmp-dev libreadline-dev postgresql librsvg2-bin libsqlite3-dev zlib1g-dev
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

#### Systemd service:

```bash
$ sudo cp /home/invidious/invidious/invidious.service /etc/systemd/system/invidious.service
$ sudo systemctl enable --now invidious.service
```

#### Logrotate:

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

### MacOS:

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

Because of various issues Invidious **must** be restarted often, at least once a day, ideally every hours.

If you use a reverse proxy, you **must** configure invidious to properly serve request through it:

`https_only: true` : if your are serving your instance via https, set it to true

`domain: domain.ext`: if you are serving your instance via a domain name, set it here

`external_port: 443`: if your are serving your instance via https, set it to 443

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
