# Database migration information

When Invidious gets a new feature, sometimes it comes with database changes that
need manual intervention. Invidious comes with a `--migrate` command that does
all the migrations for you, however, migrations can go wrong.

Because of this, we recommend you to do a backup of your Invidious database before running any migrations.

We provide backup and migration instructions for:

- [Docker Compose](./db-migration-backup-docker.md): For people that installed their Invidious instance with the [Installation instructions for Docker Compose (Production)](./installation.md#docker-compose-method-production)
- [Manual installation](./db-migration-backup-manual.md): For people that installed their Invidious instance with the [Installation instructions for a manual installation](./installation.md#manual-installation)

And we also provide restore instructions for the same installations methods listed above:

- [Docker Compose](./db-migration-restore-docker.md)
- [Manual installation](./db-migration-restore-manual.md)

