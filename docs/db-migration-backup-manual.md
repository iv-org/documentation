# Database backup and migration for manual installations

This guide is divided into 4 sections:

- [Checking if you have free space to make a backup](#checking-if-you-have-free-space-to-make-a-backup)
- [Deleting cached videos to reduce the size of the backup (recommended for public instances)](#deleting-cached-videos-to-reduce-the-size-of-the-backup-recommended-for-public-instances)
- [Doing a backup](#doing-a-backup)
- [Migrating your database](#migrating-your-database)

## Checking if you have free space to make a backup

Doing a backup can take large portions of your storage if you have limited
resources (like running Invidious in a VPS), therefore you should check how many
free space you have in the server you are running Invidious on.

Follow this steps to check the size of your database:

##### 1) Stop Invidious

```bash
$ docker compose down
```

##### 2) Check the size of the database

```bash
$ sudo -i -u postgres
$ psql
# Write `SELECT pg_size_pretty(pg_database_size('invidious'));`
# into the psql interactive terminal
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

## Deleting cached videos to reduce the size of the backup (recommended for public instances)

**You can skip this step if you have enough free space**.

Invidious caches video information so it can be later reused to display video
information, this is stored in the `videos` table and all the rows can be safely
deleted to free up some space when doing the backup.

###### 1) Stop invidious

```bash
$ sudo systemctl stop invidious.service
```

###### 2) Delete the video cache

```bash
$ sudo -i -u postgres
$ psql -d invidious
# Write `TRUNCATE TABLE videos;`
# into the psql interactive terminal
invidious=# TRUNCATE TABLE videos;
# Exit the psql interactive terminal with the Ctrl+D keybind.
```

## Doing a backup

After you checked if you really have free space to make a backup, let's do a
backup!

###### 1) Stop Invidious

```bash
$ sudo systemctl stop invidious.service
```

###### 2) Dump the Invidious database

```bash
$ sudo -i -u postgres
$ pg_dump invidious > dump.sql
```

And done, if your Invidious database is big, it may take a while to finish the
`pg_dump` process.

Your backup will be saved in the current directory where the command was
executed as `dump.sql` which you can later delete if everything went fine when
migrating your database.

## Migrating your Database

### Manual installation

Go to the directory where your Invidious installation is and follow this steps:

###### 1) Go to the Invidious installation folder

```bash
$ sudo su - invidious
$ cd invidious
```

###### 2) Migrate database

```bash
$ ./invidious --migrate
```

---

And done, your Invidious instance should now be migrated to the latest database
version. If anything goes wrong, you can always restore your data reading the
[Database restore for Docker Compose installations](./db-migration-restore-docker.md)
guide.
