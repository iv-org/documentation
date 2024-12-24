# Temporary installation guide for Invidious companion 

After installation take a look at the [Post-install steps](#post-install-configuration).

Note: Any [PaaS](https://en.wikipedia.org/wiki/Platform_as_a_service) or [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service) provider/software (Heroku, YunoHost, Repli...) are unsupported. Use them at your own risk. They **WILL** cause problems with Invidious and might even suspend your account for "abuse" since Invidious is heavy, bandwidth intensive and technically a proxy (and most providers don't like them). If you use one and want to report an issue, please mention which one you use.

# WARNING about this doc

This documentation is temporary and will explain you how to test Invidious companion. Make sure to subscribe to the issue [4734](https://github.com/iv-org/invidious/issues/4734) where you will be alerted once Invidious companion is available in a stable release of Invidious!

Because once it is in stable release the special docker tag ":companion" WON'T be updated anymore!

And if you are using a reverse proxy then make sure to read again the post install because you have new routes to add!

## Hardware requirements

Running Invidious requires at least 20GB disk space, 512MB of free RAM (so ~2G installed on the system), as long as it is restarted regularly, as recommended in the post-install configuration. Public instances should ideally have at least 60G disk space, 4GB of RAM, 2vCPU, a 200 mbps link and 20TB of traffic (no data cap/unlimited traffic is preferred).

Compiling Invidious requires at least 2.5GB of free RAM (We recommend to have at least 4GB installed).
If you have less (e.g on a cheap VPS) you can setup a SWAP file or partition, so the combined amount is >= 4GB.

You need at least 1GB of RAM for the machine that will run the tool `youtube-trusted-session-generator` in the 1st step. Doesn't need to be the same machine as the one running Invidious, just a machine running on the same public IP address.

## Docker

**The Invidious docker image is only [available on Quay](https://quay.io/repository/invidious/invidious) because, unlike Docker Hub, [Quay is Free and Open Source Software](https://github.com/quay/quay/blob/master/LICENSE). This is reflected in the `docker-compose.yml` file used in this walk-through.**

Ensure [Docker Engine](https://docs.docker.com/engine/install) and [Docker Compose](https://docs.docker.com/compose/install) are installed before beginning.

### Docker-compose method (production)

**This method uses the pre-built Docker image from quay**

Note: Currently the repository has to be cloned, this is because the `init-invidious-db.sh` file and the `config/sql` directory have to be mounted to the postgres container (See the volumes section in the docker-compose file below). This "problem" will be solved in the future.

Make sure to run the newer Docker Compose V2: https://docs.docker.com/compose/install/linux/. It should already be installed if you can successfully run the command `docker compose` (with a space between the two words).


1.  Execute these commands:
    ```bash
    git clone https://github.com/iv-org/invidious.git
    cd invidious
    ```

2.  Edit the docker-compose.yml with this content:

    ```docker
    version: "3"
    services:

      invidious:
        image: quay.io/invidious/invidious:companion
        # image: quay.io/invidious/invidious:companion-arm64 # ARM64/AArch64 devices
        restart: unless-stopped
        ports:
          - "127.0.0.1:3000:3000"
        environment:
          # Please read the following file for a comprehensive list of all available
          # configuration options and their associated syntax:
          # https://github.com/iv-org/invidious/blob/master/config/config.example.yml
          INVIDIOUS_CONFIG: |
            db:
              dbname: invidious
              user: kemal
              password: kemal
              host: invidious-db
              port: 5432
            check_tables: true
            invidious_companion:
            - private_url: "http://companion:8282/" # URL used for the internal communication between invidious and invidious companion
              public_url: "http://localhost:8282/" # (public) URL used for the communication between your browser and invidious companion
            invidious_companion_key: "CHANGE_ME!!"
            # external_port:
            # domain:
            # https_only: false
            # statistics_enabled: false
            hmac_key: "CHANGE_ME!!"
        healthcheck:
          test: wget -nv --tries=1 --spider http://127.0.0.1:3000/api/v1/trending || exit 1
          interval: 30s
          timeout: 5s
          retries: 2
        logging:
          options:
            max-size: "1G"
            max-file: "4"
        depends_on:
          - invidious-db

      invidious_companion:
        image: quay.io/invidious/invidious-companion:latest
        environment:
          - SECRET_KEY=CHANGE_ME!!SAME_AS_INVIDIOUS_COMPANION_SECRET_KEY_FROM_INVIDIOUS_CONFIG 
        #  - BASE_URL=http://localhost:8282 # ONLY use if you are using a reverse proxy - this the same URL as "public_url"
        restart: unless-stopped
        ports:
          - "127.0.0.1:8282:8282"
        logging:
          options:
            max-size: "1G"
            max-file: "4"
        cap_drop:
          - ALL
        read_only: true
        user: 10001:10001
        # cache for youtube library
        volumes:
          - /var/tmp/youtubei.js:/var/tmp/youtubei.js:rw
        security_opt:
          - no-new-privileges:true

      invidious-db:
        image: docker.io/library/postgres:14
        restart: unless-stopped
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

    volumes:
      postgresdata:
    ```

    Note: This compose is made for a true "production" setup, where Invidious is behind a reverse proxy. If you prefer to directly access Invidious, replace `127.0.0.1:3000:3000` with `3000:3000` under the `ports:` section.

3. Run the docker composition:

```
docker compose up -d
```


### Docker-compose method (development)

**This method builds a Docker image from source**

```bash
git clone https://github.com/iv-org/invidious.git
cd invidious
docker-compose up
```


## Manual Installation

### Linux

#### Install Crystal

Follow the instructions for your distribution here: https://crystal-lang.org/install/

**Note:** Invidious currently supports the following Crystal versions: `1.10.x` / `1.11.x` / `1.12.x`. \
Versions `1.9.x` and older are incompatible because we use features only present in the newer versions. \
Versions `1.13.x` should be compatible, however we did not test it.

#### Install the dependencies

Arch Linux
```bash
sudo pacman -S base-devel librsvg postgresql ttf-opensans
```

Debian/Ubuntu
```bash
sudo apt install libssl-dev libxml2-dev libyaml-dev libgmp-dev libreadline-dev postgresql librsvg2-bin libsqlite3-dev zlib1g-dev libpcre3-dev libevent-dev fonts-open-sans
```

RHEL based and RHEL-like systems (RHEL, Fedora, AlmaLinux, RockyLinux...)
```bash
sudo dnf install -y openssl-devel libevent-devel libxml2-devel libyaml-devel gmp-devel readline-devel postgresql librsvg2-devel sqlite-devel zlib-devel gcc  open-sans-fonts
```

#### Add an Invidious user and clone the repository

```bash
useradd -m invidious
su - invidious
git clone https://github.com/iv-org/invidious
exit
```

#### Set up PostgreSQL

```bash
systemctl enable --now postgresql
sudo -i -u postgres
psql -c "CREATE USER kemal WITH PASSWORD 'kemal';" # Change 'kemal' here to a stronger password, and update `password` in config/config.yml
createdb -O kemal invidious
exit
```

#### Set up Invidious

```bash
su - invidious
cd invidious
make

# Configure config/config.yml as you like
cp config/config.example.yml config/config.yml 

# edit config.yaml to include invidious companion

edit config/config.yaml

add:
invidious_companion:
- private_url: "http://companion:8282/" # URL used for the internal communication between invidious and invidious companion
  public_url: "http://localhost:8282/" # (public) URL used for the communication between your browser and invidious companion

# Deploy the database
./invidious --migrate

exit
```

#### Systemd service for Invidious

```bash
cp /home/invidious/invidious/invidious.service /etc/systemd/system/invidious.service
systemctl enable --now invidious.service
```

#### Set up Invidious companion

```bash
wget https://github.com/iv-org/invidious-companion???

# or compile it using https://docs.deno.com/runtime/
git clone https://github.com/iv-org/invidious-companion.git
deno compile

# create a new systemd service for running it
sudo wget https://github.com/iv-org/invidious-companion/raw/refs/heads/master/systemd.service -O /etc/systemd/systemd/invidious-companion.service
sudo systemctl enable --now invidious.service
```

### MacOS

#### Install the dependencies

```bash
brew update
brew install crystal postgresql imagemagick librsvg
```

#### Clone the Invidious repository

```bash
git clone https://github.com/iv-org/invidious
cd invidious
```

#### Set up PostgreSQL

```bash
brew services start postgresql
createdb
psql -c "CREATE ROLE kemal WITH LOGIN PASSWORD 'kemal';" # Change 'kemal' here to a stronger password, and update `password` in config/config.yml
createdb -O kemal invidious
psql invidious kemal < config/sql/channels.sql
psql invidious kemal < config/sql/videos.sql
psql invidious kemal < config/sql/channel_videos.sql
psql invidious kemal < config/sql/users.sql
psql invidious kemal < config/sql/session_ids.sql
psql invidious kemal < config/sql/nonces.sql
psql invidious kemal < config/sql/annotations.sql
psql invidious kemal < config/sql/playlists.sql
psql invidious kemal < config/sql/playlist_videos.sql
```

#### Set up Invidious

```bash
make

# Configure config/config.yml as you like
cp config/config.example.yml config/config.yml

# edit config.yaml to include invidious companion

edit config/config.yaml

add:
invidious_companion:
- private_url: "http://companion:8282/" # URL used for the internal communication between invidious and invidious companion
  public_url: "http://localhost:8282/" # (public) URL used for the communication between your browser and invidious companion

# launch invidious
./invidious
```

#### Set up Invidious companion

```bash
wget https://github.com/iv-org/invidious-companion???

# or compile it using https://docs.deno.com/runtime/
git clone https://github.com/iv-org/invidious-companion.git
deno compile

# launch it
./invidious-companion
```

### Windows

Crystal, the programming language used by Invidious, [doesn't officially support Windows yet](https://github.com/crystal-lang/crystal/issues/5430) but you can still install Invidious:

- By installing [Docker desktop](https://docs.docker.com/desktop/install/windows-install/) and then following [our guide about Docker](#docker).
- By installing [Windows Subsystem for Linux](https://msdn.microsoft.com/en-us/commandline/wsl/about) and then following [our guide about Linux](#linux).
- By installing [Windows-specific builds](https://github.com/crystal-lang/crystal/releases/) of Crystal. Be wary, as we don't currently have records of Invidious being tested on those "unsupported" builds yet.

## Post-install configuration:

Detailed configuration available in the [configuration guide](./configuration.md).

You must set a random generated value for the parameter `hmac_key:`! On Linux you can generate it using the command `pwgen 20 1`.

Because of various issues, Invidious **must** be restarted often, at least once a day, ideally every hour.

If you use a reverse proxy, you **must** configure Invidious to properly serve request through it:

`https_only: true` : if you are serving your instance via https, set it to true

`domain: domain.ext`: if you are serving your instance via a domain name, set it here

`external_port: 443`: if you are serving your instance via https, set it to 443

`use_pubsub_feeds: true`: if you are serving your instance on the internet, allow for faster notification of new videos ([detailed explanation](https://github.com/iv-org/invidious/blob/97c4165f55c4574efb554c9dae8d919d08da1cdd/config/config.example.yml#L409)).

`use_innertube_for_captions: true`: if you are serving a public instance or you are hosting Invidious in a datacenter, allow to unblock captions ([detailed explanation](https://github.com/iv-org/invidious/issues/2567#issuecomment-1727928996)).

AND make sure to add these new routes into your reverse proxy, example in various reverse proxy:

- [NGINX](./companion-nginx.md)
- [Apache2](./companion-apache2.md)
- [Caddy](./companion-caddy.md)

## Update Invidious

#### Updating a Docker install
```bash
docker-compose pull
docker-compose up -d
docker image prune -f
```

#### Update a manual install
```bash
su - invidious
cd invidious
git pull
make
exit
systemctl restart invidious.service
```

## Usage:

```bash
./invidious
```


#### Logrotate configuration

```bash
echo "/home/invidious/invidious/invidious.log {
rotate 4
weekly
notifempty
missingok
compress
minsize 1048576
}" | tee /etc/logrotate.d/invidious.logrotate
chmod 0644 /etc/logrotate.d/invidious.logrotate
```
