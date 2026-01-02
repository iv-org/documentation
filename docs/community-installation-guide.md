# Community Installation Guide

??? warning "Before following the community installation guide"
    All the platforms listed in the community installation guide are not supported officially by the Invidious developers.  
    This means:   

    - The Invidious developers can't help you to solve issues with your platform. Ask the community on [Matrix](https://matrix.to/#/#invidious:matrix.org) or [IRC](https://web.libera.chat/?channel=#invidious) before creating GitHub issues. But if you do fix an issue please create a PR for updating the community installation guide.
    - The guide for your platform may be outdated because things have changed since the creation of the guide.

If your platform is not listed but you would like to contribute to this guide for adding it, please do [here](https://github.com/iv-org/documentation/edit/master/docs/community-installation-guide.md). We rely on the community to help us.

After installation take a look at the [Post-install steps](installation.md#post-install-configuration).

## Podman (rootless container)

Guide contributor(s): [@sigulete](https://github.com/sigulete)

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
--health-cmd="wget -nv --tries=1 --spider http://127.0.0.1:3000/api/v1/stats || exit 1" \
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

Guide contributor(s): [@redbeardymcgee](https://git.mcgee.red/redbeardymcgee)

This method employs rootless containers through podman whose lifecycles are managed by systemd and is suitable for systems which come with Podman version 5.x or higher. Ensure that SELinux is in enforcing mode for maximum security. Do not run any of the following commands or scripts as root.

### Define containers

Add the quadlet definitions for Invidious, the database, and the companion containers to `$HOME/.config/containers/systemd/invidious`.

```ini
# $HOME/.config/containers/systemd/invidious/invidious.container
[Unit]
Description=Invidious
Requires=invidious-db.service
After=invidious-db.service
Requires=invidious-companion.service
After=invidious-companion.service

[Service]
Restart=on-failure
TimeoutStartSec=900

[Install]
WantedBy=multi-user.target

[Container]
Image=quay.io/invidious/invidious:latest
ContainerName=invidious
AutoUpdate=registry

Network=invidious.network
HostName=invidious

Volume=./config.yml:/invidious/config/config.yml:Z
```

```ini
# $HOME/.config/containers/systemd/invidious/invidious-db
[Unit]
Description=Invidious postgres

[Service]
Restart=on-failure
TimeoutStartSec=900

[Install]
WantedBy=multi-user.target

[Container]
Image=docker.io/library/postgres:14
ContainerName=invidious-db
AutoUpdate=registry

Network=invidious.network
HostName=invidious-db

Volume=invidious-db:/var/lib/postgresql/data:Z

Environment=POSTGRES_DB=invidious
Environment=POSTGRES_USER=kemal
Environment=POSTGRES_PASSWORD=kemal

# NOTE: Alternatively, set password as a podman secret
# `printf 'my-postgres-password' | podman secret create --replace invidious-db-pw -`
# Secret=invidious-db-pw,type=env,target=POSTGRES_PASSWORD
```

```ini
# $HOME/.config/containers/systemd/invidious/invidious-companion
[Unit]
Description=Invidious companion

[Service]
Restart=on-failure
TimeoutStartSec=900

[Install]
WantedBy=multi-user.target

[Container]
Image=quay.io/invidious/invidious-companion:latest
ContainerName=invidious-companion
AutoUpdate=registry

Network=invidious.network
HostName=invidious-companion

Volume=invidious-companion-cache:/var/tmp/youtubei.js:rw,Z

# WARNING: The container will fail to start without this env var
# NOTE: The podman secret is preferred, but you may set the env var directly like this
# Environment=SERVER_SECRET_KEY=my-secret-key

# If you set the env var above, comment this out
# `pwgen 16 1 | podman secret create --replace invidious-db-pw -`
Secret=invidious-companion-secret-key,type=env,target=SERVER_SECRET_KEY
```

### Define the storage volumes

The database requires a data volume to persist the database. The companion uses a cache volume.

```ini
# $HOME/.config/containers/systemd/invidious/invidious-db.volume
[Volume]
VolumeName=invidious-db
```

```ini
# $HOME/.config/containers/systemd/invidious/invidious-companion.volume
[Volume]
VolumeName=invidious-companion-cache
```

### Modify `config.yml` for your evironment

Copy the example config from [HERE](https://github.com/iv-org/invidious/blob/master/config/config.example.yml).

`curl -o "$HOME"/.config/containers/systemd/invidious/config.yml https://raw.githubusercontent.com/iv-org/invidious/refs/heads/master/config/config.example.yml`

Edit the configuration according to your environment. The example is very well commented. Notable fields include `invidious_companion` and `invidious_companion_key` to ensure that the companion container is connectable. If you changed the `$POSTGRES_PASSWORD`, then it should be configured to match in the `db` field. The field `hmac_key` is **mandatory**.

!!! warning

    The Invidious container may fail to start or operate as expected if the `config.yml` is not correctly configured.

### Confirm the container services are generated

Systemd units are generated on-the-fly during `daemon-reload` command, but before that let's check syntax with quadlet generator. Note, you need Podman version 5.0 or higher, older versions will not work:

`QUADLET_UNIT_DIRS="$HOME/.config/containers/systemd/invidious" /lib/systemd/user-generators/podman-user-generator -user -dryrun`

Reload systemd daemon. Keep in mind you need to do this command every time you change a unit file.

`systemctl --user daemon-reload`

### Prepare the database

The database container requires an initial migration. This should be handled by the field `check_tables` in `config.yml` if set to `true`. The following steps will manually initialize the database in case there is an issue.

```bash
# Start the database container
systemctl --user start invidious-db

# Enter the container, install curl, initialize the database, uninstall curl
podman exec invidious-db \
  sh -c '
        apt-get update
        apt-get install --assume-yes --no-install-recommends curl

        for initdb in channels videos channel_videos users session_ids nonces annotations playlists playlist_videos
        do
          curl -s https://raw.githubusercontent.com/iv-org/invidious/refs/heads/master/config/sql/$initdb.sql | psql postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@invidious-db/$POSTGRES_DB
        done
        apt-get --assume-yes purge curl
        '
```

### Create a timer to restart Invidious regularly

Invidious recommends restarting frequently in the [post-install configuration documentation](https://docs.invidious.io/installation/#post-install-configuration). A systemd timer is an effective method of achieving this. Add the file to `$HOME/.config/systemd/user/invidious.timer` and activate it with `systemctl --user enable --now invidious.timer`.

```ini
# $HOME/.config/systemd/user/invidious.timer
[Unit]
Description=Restart Invidious every hour

[Install]
WantedBy=timers.target

[Timer]
OnUnitActiveSec=60minutes
```

### Start the application

And the whole application can be now started:

`systemctl --user start invidious`

Keep in mind that generated units cannot be enabled using `systemctl --user enable`. The Invidious containers will be started automatically.

## MacOS

Looking for contributors to this operating system. Please submit a new doc for MacOS at https://github.com/iv-org/documentation/blob/master/docs/community-installation-guide.md

## BSD (FreeBSD - OpenBSD)

People have successfully ran Invidious on FreeBSD/OpenBSD as discussed in https://github.com/iv-org/invidious/issues/2388

We are looking for contributors to write a proper guide for installing Invidious on FreeBSD/OpenBSD. If you can, please submit a new doc for FreeBSD/OpenBSD at https://github.com/iv-org/documentation/blob/master/docs/community-installation-guide.md
