# Community Installation Guide

??? warning "Before following the community installation guide"
    All the platforms listed in the community installation guide are not supported officially by the Invidious developers.  
    This means:   

    - The Invidious developers can't help you to solve issues with your platform. Ask the community on [Matrix](https://matrix.to/#/#invidious:matrix.org) or [IRC](https://web.libera.chat/?channel=#invidious) before creating GitHub issues. But if you do fix an issue please create a PR for updating the community installation guide.
    - The guide for your platform may be outdated because things have changed since the creation of the guide.

If your platform is not listed but you would like to contribute to this guide for adding it, please do [here](https://github.com/iv-org/documentation/edit/master/docs/community-installation-guide.md). We rely on the community to help us.

After installation take a look at the [Post-install steps](installation.md#post-install-configuration).

## Podman (rootless container)

Podman is usually pre-installed in Fedora, CentOS, RHEL and derivatives. But if this is not the case, the instruction below will install all necessary packages.

RHEL based and RHEL-like systems
```bash
sudo dnf install podman
```

### Download the configuration files from Invidious' repository

Note: Currently the repository has to be cloned, this is because the `init-invidious-db.sh` file and the `config/sql` directory have to be mounted to the postgres container (See the volumes section in the postgres' container). This "problem" will be solved in the future.
> `<INV-PATH>` Absolute path in your home directory where Invidious will be downloaded (e.i. /home/johnsmith/.inv)

```bash
cd <INV-PATH>
git clone https://github.com/iv-org/invidious.git
```

### Create Pod - videos

```bash
podman pod create --name videos -p 3000:3000
```

### Create Container - postgres

```bash
podman create --rm \
--pod videos \
--name postgres \
--label "io.containers.autoupdate=registry" \
--health-cmd='pg_isready -U $POSTGRES_USER -d $POSTGRES_DB' \
-v postgresdata:/var/lib/postgresql/data \
-v <INV-PATH>/invidious/config/sql:/config/sql:z \
-v <INV-PATH>/invidious/docker/init-invidious-db.sh:/docker-entrypoint-initdb.d/init-invidious-db.sh:z \
-e POSTGRES_DB=invidious \
-e POSTGRES_USER=kemal \
-e POSTGRES_PASSWORD=kemal \
docker.io/library/postgres:14
```

### Create Container - invidious

Copy `<INV-PATH>/invidious/config/config.example.yml` to `<INV-PATH>/config.yml` and update parameters as required.

```bash
podman create --rm \
--pod videos \
--name invidious \
--label "io.containers.autoupdate=registry" \
--health-cmd="wget -nv --tries=1 --spider http://127.0.0.1:3000/api/v1/trending || exit 1" \
--health-interval=30s \
--health-timeout=5s \
--health-retries=2 \
-v <INV-PATH>/config.yml:/invidious/config/config.yml:z,U \
quay.io/invidious/invidious:latest
```

### Create systemd services to manage the Pod

Podman can generate systemd services to handle the life cycle of pods and containers. 
The instructions below will create 3 service units, and they will be placed in the correct location ready to be used.

```bash
cd ~
cp $(podman generate systemd --new --files --name videos) .config/systemd/user
```

### Start Pod

Despite the existance of 3 services, only the one related to the Pod must be used. The life cycle for the 2 containers implementing **postgres** and **invidious** will be handled by the pod.

```bash
systemctl --user daemon-reload
systemctl --user enable --now pod-videos.service
```

And similarly, the instruction below will re-start the service:

```bash
systemctl --user restart pod-videos.service
```

If this service runs on a server, it will stop as soon as you logout, because it is running in user space. 
To ensure it is persistent and remains active after logging out, you will need to enable user lingering.

```bash
loginctl enable-linger
```

### Updating to the latest release

```bash
podman auto-update
podman image prune -f
```

## Podman via systemd

This method is suitable for systems which come with Podman version 5.x or higher and systemd (e.g. Fedora, CentOS Stream 9 or clones). Instructions are written for root-less mode, do not run the commands as root since paths are different. Ensure that SELinux is in enforcing mode for maximum security.

Create a new volume for database:

    podman volume create invidious-db

Start a temporary container:

    podman run --rm -it --name invidious-init -v invidious-db:/var/lib/postgresql/data:Z -p 5432:5432 -e POSTGRES_DB=invidious -e POSTGRES_USER=kemal -e POSTGRES_PASSWORD=kemal docker.io/library/postgres:14

In another terminal, migrate the database:

    export PGPASSWORD=kemal
    for F in channels videos channel_videos users session_ids nonces annotations playlists playlist_videos; do
        curl -s https://raw.githubusercontent.com/iv-org/invidious/refs/heads/master/config/sql/$F.sql | \
            psql -h localhost -p 5432 -U kemal invidious
    done

Shutdown the temporary container, it is no longer needed. Create a database volume unit:

    cat > ~/.config/containers/systemd/invidious-db.volume <<EOF
    [Volume]
    VolumeName=invidious-db
    EOF

And a database container:

    cat > ~/.config/containers/systemd/invidious-db.container <<EOF
    [Container]
    ContainerName=invidious-db
    Environment=POSTGRES_DB=invidious POSTGRES_USER=kemal POSTGRES_PASSWORD=kemal
    Image=docker.io/library/postgres:14
    HealthCmd=pg_isready -h localhost -p 5432 -U kemal -d invidious
    Notify=healthy
    Pod=invidious.pod
    Volume=invidious-db.volume:/var/lib/postgresql/data:Z
    EOF

Create a helper container:

    cat > ~/.config/containers/systemd/invidious-sig-helper.container <<EOF
    [Container]
    ContainerName=invidious-sig-helper
    Environment=RUST_LOG=info
    Image=quay.io/invidious/inv-sig-helper:latest
    Exec=--tcp 0.0.0.0:12999
    Pod=invidious.pod
    EOF

Generate your `VISITOR_DATA` an `PO_TOKEN` secrets. For more information about these, read the information dialog above.

    podman run quay.io/invidious/youtube-trusted-session-generator

Set those secrets as temporary environmental variables, also generate a random string for HMAC secret:

    HMAC=$(openssl rand -base64 21)
    VISITOR_DATA="ABCDEF%3D%3D" # notsecret
    PO_TOKEN="MpOIfiljfsdljds-Lljfsdk-ojrdjXVs==" # notsecret

In the same terminal where you defined the environmental variables, create new environmental config file:

    cat > ~/.config/containers/systemd/invidious.env <<EOF
    INVIDIOUS_DATABASE_URL="postgres://kemal:kemal@invidious-db:5432/invidious"
    #INVIDIOUS_CHECK_TABLES=true
    #INVIDIOUS_DOMAIN="inv.example.com"
    INVIDIOUS_SIGNATURE_SERVER="invidious-sig-helper:12999"
    INVIDIOUS_VISITOR_DATA="$VISITOR_DATA"
    INVIDIOUS_PO_TOKEN="$PO_TOKEN"
    INVIDIOUS_HMAC_KEY="$HMAC"
    EOF

From now on, if you need to change configuration just edit the generated file `~/.config/containers/systemd/invidious.env`. Now, create Invidious container unit:

    cat > ~/.config/containers/systemd/invidious.container <<EOF
    [Container]
    ContainerName=invidious
    EnvironmentFile=%h/.config/containers/systemd/invidious.env
    Image=quay.io/invidious/invidious:latest
    Pod=invidious.pod
    [Unit]
    After=invidious-db.service
    EOF

And finally, create pod unit. Note only port 3000 is exposed, do not expose other ports!

    cat > ~/.config/containers/systemd/invidious.pod <<EOF
    [Pod]
    PodName=invidious
    PublishPort=3000:3000
    [Install]
    WantedBy=multi-user.target default.target
    EOF

Systemd units are generated on-the-fly during `daemon-reload` command, but before that let's check syntax with quadlet generator. Note, you need Podman version 5.0 or higher, older versions will not work:

    /usr/libexec/podman/quadlet -dryrun -user

Reload systemd daemon. Keep in mind you need to do this command every time you change a unit file, you can change the environmental file freely tho.

    systemctl --user daemon-reload

And the whole application can be now started:

    systemctl --user start invidious-pod

Keep in mind that generated units cannot be enabled using `systemctl enable`, the main pod will be enabled automatically. If you do not like this behavior, remove the `WantedBy` line from `invidious.pod`.

## MacOS

### Generate po_token and visitor_data identities

[Follow these instructions here on the official tool `youtube-trusted-session-generator`](https://github.com/iv-org/youtube-trusted-session-generator?tab=readme-ov-file#tutorial-without-docker)

These two parameters will be required for passing all verification checks on YouTube side and you will have to configure them in Invidious.

You have to run this command on the same public IP address as the one blocked by YouTube. Not necessarily the same machine, just the same public IP address.  
You will need to copy these two parameters in the `config.yaml` file.  
Subsequent usage of this same token will work on the same IP range or even the same ASN. The point is to generate this token on a blocked IP as "unblocked" IP addresses seems to not generate a token valid for passing the checks on a blocked IP.  

??? warning "About po_token and visitor_data identities"

    po_token known as Proof of Origin Token. This is an attestation token generated by a complex anti robot verification system created by Google named BotGuard/DroidGuard. It is used to confirm that the request is coming from a genuine device.
    
    These identity tokens (po_token and visitor_data) generated in this tutorial will make your entire Invidious session more easily traceable by YouTube because it is tied to a unique identifier.
    
    There is currently no official automatic tool to periodically change these tokens. This is working in progress but, for the time being, this is the solution the Invidious team is offering.

    If you want to be less traceable, you can always script the process by changing the identities every X hour.

### Run inv_sig_helper in background

[Follow these instructions here on the official tool `inv_sig_helper`](https://github.com/iv-org/inv_sig_helper?tab=readme-ov-file#building-and-running-without-docker)

inv_sig_helper handle the "deciphering" of the video stream fetched from YouTube servers. As it is running untrusted code from Google themselves, make sure to isolate it by for example running it inside Docker or a VM.

Call for action: An example here is welcome, [if you want to contribute to one](https://github.com/iv-org/documentation/edit/master/docs/installation.md#macos).

### Install the dependencies

```bash
brew update
brew install crystal postgresql imagemagick librsvg
```

### Clone the Invidious repository

```bash
git clone https://github.com/iv-org/invidious
cd invidious
```

### Set up PostgreSQL

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

### Set up Invidious

```bash
make

# Configure config/config.yml as you like
cp config/config.example.yml config/config.yml

# edit config.yaml to include po_token and visitor_data previously generated

edit config/config.yaml
```