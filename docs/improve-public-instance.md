# Improve your public instance performance and stability

This tutorial has been written by [unixfox](https://github.com/unixfox), owner of [yewtu.be](https://yewtu.be/). He is better suited when looking for help about this tutorial.

## Synopsis

This tutorial will explain how to improve the performance, and decrease the memory and CPU consumption of your public instance on your server.

Using Docker is recommended for this tutorial because the process is simpler with it. You can try it outside of Docker by adapting the ideas of this tutorial, but the main focus will be Docker.

## Instructions

### 1) Tune up your config.yml

For decreasing the load on the PostgreSQL database:

- enable_user_notifications: false  
  User notifications will be deactivated.  
  On large instances, it is recommended to set this option to `false` in order to reduce the amount of data written to the database, and hence improve the overall performance of the instance.

### 2) Multiple Invidious processes

Invidious is single threaded, so by running multiple processes you better utilize the multiple threads of your server.  
Also past a certain amount of requests, Invidious becomes sluggish. Having multiple processes reduces this sluggishness.

This tutorial will explain how to run multiple containers of Invidious and use NGINX in Docker as a loadbalancer.  
If your reverse proxy is already in Docker you can also adapt it so that it sends the requests directly to the Invidious containers.

We assume that you have not changed the port `3000` from the default installation. But if you changed it then you will need to adapt it in the following configuration files and commands.

1. In your `docker-compose.yml`, remove these lines for binding the port of Invidious:
   ```
   ports:
    - "127.0.0.1:3000:3000"
   ```
2. Duplicate the whole "invidious service" and copy it into a new one named `invidious-refresh`.  
   Yes the whole block from the "invidious service". From `invidious:` to `- invidious-db`.
3. Add these two lines into your `INVIDIOUS_CONFIG` parameter for **only the invidious service**:
   ```
   channel_threads: 0
   feed_threads: 0
   jobs:
     clear_expired_items:
       enabled: false
     refresh_channels:
       enabled: false
     refresh_feeds:
       enabled: false
   ```
   This is required so that only one invidious process refresh the subscriptions for the users.  
   Running this process with multiple processes may introduce some conflicts.
4. Edit the docker-compose.yml with this content:
   ```
   version: "3"
   services:
      invidious:
         image: quay.io/invidious/invidious:latest
         deploy:
            replicas: 6
   ```
   Explanation: The `deploy.replicas` parameter allows running multiple containers of the same Docker image.  
   Note: You can set more or less Invidious processes (6 in the example).  
   **Don't restart Invidious yet!**
5. Create a file called `nginx.conf` and add this content:
   ```
   user www-data;
   events {
        worker_connections 1000;
   }
   http {
        server {
            listen 3000;
            listen [::]:3000;
            access_log off;
            location / {
                resolver 127.0.0.11;
                set $backend "invidious";
                proxy_pass http://$backend:3000;
                proxy_http_version 1.1; # to keep alive
                proxy_set_header Connection ""; # to keep alive
            }
        }
   }
   ```
6. Add a new service in your `docker-compose.yml` file:
   ```
   nginx:
      image: nginx:latest
      restart: unless-stopped
      volumes:
        - ./nginx.conf:/etc/nginx/nginx.conf:ro
      depends_on:
        - invidious
      ports:
        - "127.0.0.1:3000:3000"
   ```
7. Update your cronjobs to restart Invidious (if you use cron).
   Instead of restarting a single Docker container you will now need to restart 6 containers (adjust if you added or removed number of containers).
   Replace with these CRON lines:
   ```
   0 */1 * * * docker restart invidious-invidious-1
   1 */1 * * * docker restart invidious-invidious-2
   2 */1 * * * docker restart invidious-invidious-3
   3 */1 * * * docker restart invidious-invidious-4
   4 */1 * * * docker restart invidious-invidious-5
   5 */1 * * * docker restart invidious-invidious-6
   ```
   Each CRON line has a different schedule to avoid disrupting your entire Invidious instance due a restart.
8. Apply the new configuration:
   ```
   docker compose down
   docker compose up
   ```

??? note "Click here for a final example of the `docker-compose` file. (Don't copy blindly)"

    ```yaml
    version: "3"
    services:
        invidious:
            image: quay.io/invidious/invidious:latest
            deploy:
                replicas: 6
            restart: unless-stopped
            environment:
                INVIDIOUS_CONFIG: |
                    channel_threads: 0
                    feed_threads: 0
                    db:
                        dbname: invidious
                        user: kemal
                        password: kemal
                        host: invidious-db
                        port: 5432
                    check_tables: true
                    use_pubsub_feeds: true
                    use_innertube_for_captions: true
                    external_port: 443
                    domain: mydomain.com
                    https_only: true
                    statistics_enabled: true
                    hmac_key: "CHANGE_ME!!"
                    jobs:
                      clear_expired_items:
                        enabled: false
                      refresh_channels:
                        enabled: false
                      refresh_feeds:
                        enabled: false
            healthcheck:
                test: wget -nv --tries=1 --spider http://127.0.0.1:3000/api/v1/stats || exit 1
                interval: 30s
                timeout: 5s
                retries: 2
            logging:
                options:
                    max-size: "1G"
                    max-file: "4"
            depends_on:
               - invidious-db

        
        invidious-refresh:
            image: quay.io/invidious/invidious:latest
            restart: unless-stopped
            environment:
                INVIDIOUS_CONFIG: |
                    db:
                        dbname: invidious
                        user: kemal
                        password: kemal
                        host: invidious-db
                        port: 5432
                    check_tables: true
                    use_pubsub_feeds: true
                    use_innertube_for_captions: true
                    external_port: 443
                    domain: mydomain.com
                    https_only: true
                    statistics_enabled: true
                    hmac_key: "CHANGE_ME!!"
            healthcheck:
                test: wget -nv --tries=1 --spider http://127.0.0.1:3000/api/v1/stats || exit 1
                interval: 30s
                timeout: 5s
                retries: 2
            logging:
                options:
                    max-size: "1G"
                    max-file: "4"
            depends_on:
               - invidious-db 

        nginx:
            image: nginx:latest
            restart: unless-stopped
            volumes:
                - ./nginx.conf:/etc/nginx/nginx.conf:ro
            depends_on:
                - invidious
            ports:
                - "127.0.0.1:3000:3000"

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
