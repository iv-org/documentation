Invidious needs one PostgreSQL database with five tables.

`channel_videos`  
`channels`  
`nonces`  
`users`  
`videos`  

The table `videos` grows a lot and needs the most storage. You can clean it up using following commands:
```bash
$ sudo -i -u postgres
$ psql invidious -c "TRUNCATE TABLE videos"
$ exit
```