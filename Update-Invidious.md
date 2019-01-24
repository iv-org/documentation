## Invidious releases are based on tags. You can use them if you want to be sure your instance is stable.

#### With release tags
```bash
$ sudo -i -u invidious
$ cd invidious
$ git pull
$ latestVersion=$(git describe --tags `git rev-list --tags --max-count=1`)
$ git checkout $latestVersion
$ shards
$ crystal build src/invidious.cr --release
$ exit
$ sudo systemctl restart invidious.service
```

#### With master branch
```bash
$ sudo -i -u invidious
$ cd invidious
$ git pull
$ shards
$ crystal build src/invidious.cr --release
$ exit
$ sudo systemctl restart invidious.service
```