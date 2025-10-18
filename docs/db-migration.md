# Database migration

When Invidious gets a new feature, sometimes it comes with database changes that
need manual intervention. Invidious comes with a `--migrate` command that does
all the migrations for you, however, migrations can go wrong so it's recommended
to do a backup of your Invidious database before migrating your database.

This guide is divided into 4 sections:

- [Checking if you have free space to make a backup](#Checking-if-you-have-free-space-to-make-a-backup)
- [Doing a backup](#Doing-a-backup)
- [Migrating your database](#Migrating-your-database)
- [Recovering your database from a backup](#Recovering-your-database-from-a-backup):
  This step is optional and you should read it if your database migration has
  gone wrong.

## Checking if you have free space to make a backup

Doing a backup can take large portions of your storage if you have limited
resources (like running Invidious in a VPS), therefore you should check how many
free space you have in the server you are running Invidious on.

Use one of the two methods listed bellow, this will depend of how you decided to
install Invidious from the [Installation instructions](./installation.md).

### Docker

If you are using docker, execute this command to check the size of your
database:

```bash
$ docker system df -v | grep postgresdata
```

And you will get:

```
invidious_postgresdata 1 2.48GB
```

In this example, `2.48GB` is the size the database.

If you system has less free space than the value that you got, you should free
some space before making a backup.

### Manual Installation

Assuming you already have PostresSQL installed from the
[Installation instructions](./installation.md), execute this command to check
the size of your database:

```bash
$ sudo -i -u postgres
$ psql
# Write `SELECT pg_size_pretty(pg_database_size('invidious'));` into the psql interactive terminal
postgres=# SELECT pg_size_pretty(pg_database_size('invidious'));
```

And you will get:

```postgres
 pg_size_pretty
----------------
  2 GB
```

In this example, `2 GB` is the size the database.

If you system has less free space than the value that you got, you should free
some space before making a backup.

## Doing a backup

After you checked if you really have free space to make a backup, let's do a
backup!

Use one of the two methods listed bellow, this will depend of how you decided to
install Invidious from the [Installation instructions](./installation.md).

### Docker

###### 1) Stop Invidious

Go to the directory where the `docker-compose.yml` of Invidious is and use:

```bash
$ docker compose down
```

If you are hosting a public instance, make sure to make your instance
inaccessible from the internet.

###### 2) Clone the Docker Volume

Since all the data of the database is inside a Docker Volume, you just need to
copy the volume into a new one using:

```bash
$ sudo cp -ra /var/lib/docker/volumes/invidious_postgres /var/lib/docker/volumes/invidious_postgres_backup
```

###### 3) Restart Docker

In order to make Docker able to detect the backup Docker Volume, you must
restart Docker using:

```bash
$ sudo systemctl restart docker.service
```

###### 4) Check that Docker detects the volume

Now check that Docker detects the backup volume using:

```
$ docker volume ls | grep invidious_postgresdata
```

If you get something like this:

```
local     invidious_postgresdata
local     invidious_postgresdata_backup # <- Your backup!
```

Then your backup volume is detected by Docker.

###### 5) Checking your backup

Now you should check if you backup really works before proceeding to the
migration.

To do this, modify `docker-compose.yml` `volumes` declaration like this:

```
volumes:
  postgresdata:
	external: true
	name: invidious_postgresdata_backup
  companioncache:
```

And start Invidious using `docker compose up`, check some things like logging
into your account, your subscriptions and watch history, if everything loads
fine without any issues, your database is now successfully backed up and that
volume can be used to recover your database data if something goes wrong!

### Manual Installation

###### 1) Stop Invidious

```bash
$ sudo systemctl stop invidious.service
```

If you are hosting a public instance, make sure to make your instance
inaccessible from the internet.

###### 2) Dump the Invidious database

```bash
$ sudo -i -u postgres
$ pg_dump invidious | gzip > invidious-db-backup.gz
```

And done, if your Invidious database is big, it may take a while to finish the
`pg_dump` process.

## Migrating your Database

### Docker

###### 1) Start PostgreSQL

Go to the directory where the `docker-compose.yml` of Invidious is and use:

```bash
docker compose up -d invidious-db
```

###### 2) Migrate database

```bash
docker compose run invidious sh -c "./invidious --migrate"
```

## Recovering your database from a backup
