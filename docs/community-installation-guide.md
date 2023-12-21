# Community Installation Guide

After installation take a look at the [Post-install steps](installation.md#post-install-configuration).

## Podman (rootless container)

Podman is usually pre-installed in Fedora, CentOS, RHEL and derivatives. But if this is not the case, the instruction below will install all necessary packages.

RHEL based and RHEL-like systems
```bash
sudo dnf install podman
```

### Download the configuration files from Invidious' repository

Note: Currently the repository has to be cloned, this is because the `init-invidious-db.sh` file and the `config/sql` directory have to be mounted to the postgres container (See the volumes section in the postgres' container). This "problem" will be solved in the future.
> `<INV-PATH>` Absolute path in your home directory where invidious will be downloaded (e.i. /home/johnsmith/.inv)

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
--health-cmd="wget -nv --tries=1 --spider http://127.0.0.1:3000/api/v1/comments/jNQXAC9IVRw || exit 1" \
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
