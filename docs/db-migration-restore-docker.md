# Database restore for Docker Compose installations

In case a database migration went wrong, you can use a backup of your Invidious database to recover all the data or to simply revert it to a previous state.

In order to recover your Invidious database from a backup follow the next steps:

##### 1) Stop Invidious

```bash
$ docker compose down
```

##### 2) Start the database

```bash
$ docker compose up invidious-db -d
```