# Invidious Companion Installation Guide

!!! warning This is a temporary guide for testing Invidious Companion, currently in the master branch. After installation, see Post-Install Configuration for additional steps, especially if using a reverse proxy.

!!! danger Do not use PaaS/SaaS providers (e.g., Heroku, YunoHost) for Invidious. They may cause issues or suspend your account due to high bandwidth usage and proxy-like behavior. If reporting issues, specify your provider.

## Prerequisites

!!! info **Hardware**: - **Minimum**: 20GB disk space, 512MB free RAM (\~2GB total), with regular restarts (see Post-Install Configuration). - **Public Instances**: 60GB disk space, 4GB RAM, 2 vCPUs, 200 Mbps link, 20TB traffic (unlimited preferred). - **Compilation**: 2.5GB free RAM (4GB recommended). Use a SWAP file/partition on low-RAM systems (e.g., cheap VPS) to reach ≥4GB. - **youtube-trusted-session-generator**: 1GB RAM on a machine with the same public IP as Invidious.

## Docker Installation

!!! note Invidious Docker images are hosted on Quay because it’s Free and Open Source, unlike Docker Hub.

Ensure Docker Engine and Docker Compose V2 are installed. Verify by running `docker compose` (with a space).

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/iv-org/invidious.git
   cd invidious
   ```

2. **Generate Secret Keys**: Run these commands to create two unique alphanumeric keys:

   ```bash
   pwgen 16 1 # for Invidious (HMAC_KEY)
   pwgen 16 1 # for Invidious Companion (invidious_companion_key)
   ```

   !!! important Use `pwgen` to generate alphanumeric keys (letters and numbers only, no special characters) for compatibility with Invidious and Invidious Companion.

3. **Configure** `docker-compose.yml`: Create or edit `docker-compose.yml` with:

   ```yaml
   version: "3"
   services:
     invidious:
       image: quay.io/invidious/invidious:master
       # Use quay.io/invidious/invidious:master-arm64 for ARM64/AArch64
       restart: unless-stopped
       ports:
         - "127.0.0.1:3000:3000" # Change to "3000:3000" for direct access
       environment:
         INVIDIOUS_CONFIG: |
           db:
             dbname: invidious
             user: kemal
             password: kemal
             host: invidious-db
             port: 5432
           check_tables: true
           invidious_companion:
             private_url: "http://companion:8282"
             public_url: "http://localhost:8282" # Update for reverse proxy/external IP
             invidious_companion_key: "CHANGE_ME!!" # Use key from step 2
           hmac_key: "CHANGE_ME!!" # Use key from step 2
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
   
     companion:
       image: quay.io/invidious/invidious-companion:latest
       environment:
         - SERVER_SECRET_KEY=CHANGE_ME!! # Use same key as invidious_companion_key
       restart: unless-stopped
       ports:
         - "127.0.0.1:8282:8282" # Change to "8282:8282" for direct access
       logging:
         options:
           max-size: "1G"
           max-file: "4"
       cap_drop:
         - ALL
       read_only: true
       volumes:
         - companioncache:/var/tmp/youtubei.js:rw
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
     companioncache:
   ```

4. **Run Docker**:

   - For **production** (pre-built image):

     ```bash
     docker compose up -d
     ```
   - For **development** (build from source):

     ```bash
     docker compose build
     docker compose up -d
     ```

   !!! note The repository clone is required to mount `init-invidious-db.sh` and `config/sql` to the Postgres container. This will be simplified in the future.

## Manual Installation

### Linux

1. **Install Crystal**: Follow https://crystal-lang.org/install/ for your distribution. Use versions `1.10.x`, `1.11.x`, or `1.12.x` (untested `1.13.x` may work).

2. **Install Dependencies**:

   - **Arch Linux**:

     ```bash
     sudo pacman -S base-devel librsvg postgresql ttf-opensans
     ```
   - **Debian/Ubuntu**:

     ```bash
     sudo apt install libssl-dev libxml2-dev libyaml-dev libgmp-dev libreadline-dev postgresql librsvg2-bin libsqlite3-dev zlib1g-dev libpcre3-dev libevent-dev fonts-open-sans
     ```
   - **RHEL-based (RHEL, Fedora, AlmaLinux, RockyLinux)**:

     ```bash
     sudo dnf install -y openssl-devel libevent-devel libxml2-devel libyaml-devel gmp-devel readline-devel postgresql librsvg2-devel sqlite-devel zlib-devel gcc open-sans-fonts
     ```

3. **Set Up Invidious**:

   ```bash
   useradd -m invidious
   su - invidious
   git clone https://github.com/iv-org/invidious
   cd invidious
   make
   cp config/config.example.yml config/config.yml
   ```

4. **Configure PostgreSQL**:

   ```bash
   systemctl enable --now postgresql
   sudo -i -u postgres
   psql -c "CREATE USER kemal WITH PASSWORD 'kemal';" # Use a strong password
   createdb -O kemal invidious
   exit
   ```

5. **Configure Invidious**: Edit `config/config.yml`:

   ```yaml
   invidious_companion:
     private_url: "http://companion:8282"
     public_url: "http://localhost:8282" # Update for reverse proxy/external IP
     invidious_companion_key: "CHANGE_ME!!" # Use key from pwgen
   ```

   Deploy the database:

   ```bash
   ./invidious --migrate
   exit
   ```

6. **Set Up Systemd**:

   ```bash
   cp /home/invidious/invidious/invidious.service /etc/systemd/system/invidious.service
   systemctl enable --now invidious.service
   ```

7. **Set Up Invidious Companion**:

   ```bash
   git clone https://github.com/iv-org/invidious-companion.git
   cd invidious-companion
   deno task compile
   SERVER_SECRET_KEY=CHANGE_ME!! ./invidious-companion # Use same key as invidious_companion_key
   ```

   !!! info See environment variables: https://github.com/iv-org/invidious-companion/wiki/Environment-variables.

### MacOS

1. **Install Dependencies**:

   ```bash
   brew update
   brew install crystal postgresql imagemagick librsvg
   ```

2. **Set Up Invidious**:

   ```bash
   git clone https://github.com/iv-org/invidious
   cd invidious
   make
   cp config/config.example.yml config/config.yml
   ```

3. **Configure PostgreSQL**:

   ```bash
   brew services start postgresql
   createdb
   psql -c "CREATE ROLE kemal WITH LOGIN PASSWORD 'kemal';" # Use a strong password
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

4. **Configure and Run**: Edit `config/config.yml` as above, then:

   ```bash
   ./invidious
   ```

5. **Set Up Invidious Companion**: Follow the Linux steps for Invidious Companion setup.

### Windows

!!! warning Crystal lacks official Windows support (https://github.com/crystal-lang/crystal/issues/5430). Use one of these options: - Install Docker Desktop and follow the Docker Installation. - Use Windows Subsystem for Linux and follow the Linux steps. - Try Windows-specific Crystal builds, but these are untested.

## Post-Install Configuration

!!! info See the configuration guide for detailed options.

!!! danger Set a random `hmac_key` in `config/config.yml` using: `bash pwgen 20 1`

!!! warning Restart Invidious at least daily (ideally hourly) to avoid issues.

For reverse proxy setups, add these to `config/config.yml`:

```yaml
https_only: true # Enable for HTTPS
domain: domain.ext # Your domain
external_port: 443 # For HTTPS
use_pubsub_feeds: true # Faster video notifications
use_innertube_for_captions: true # Unblock captions in datacenters
```

!!! note Configure reverse proxy routes: - NGINX- Apache2- Caddy- Traefik

## Updating Invidious

### Docker

```bash
docker compose pull
docker compose up -d
docker image prune -f
```

### Manual

```bash
su - invidious
cd invidious
git pull
make
exit
systemctl restart invidious.service
```

## Usage

```bash
./invidious
```

## Log Rotation

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
