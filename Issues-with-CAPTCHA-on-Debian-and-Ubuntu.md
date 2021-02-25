---
title: Issues-with-CAPTCHA-on-Debian-and-Ubuntu
description: 
published: true
date: 2021-02-25T18:05:15.491Z
tags: 
editor: undefined
dateCreated: 2021-01-28T20:39:51.349Z
---

#### Warning: If you use ImageMagick on Ubuntu for other services like Mastodon this guide may break them, please use [this guide](https://linuxconfig.org/how-to-install-imagemagick-7-on-ubuntu-18-04-linux) instead.
There is some issue on Debian 9 and Ubuntu 18.04 and later. It appears that the clock (the CAPTCHA) has no hands but you can see them outside the clock. You need to compile ImageMagick yourself with librsvg to solve this issue.  
Thanks [Tmiland](https://github.com/tmiland) for showing up a solution at [#299](https://github.com/iv-org/invidious/issues/299)

For lazy people a little hack is to disable CAPTCHA or use text one.  

You can check if your version of ImageMagick is affected with `convert -list format`.  
It should show the following if your installed version is okay.
```
      SVG  SVG       rw+   Scalable Vector Graphics (RSVG 2.40.13)
     SVGZ  SVG       rw+   Compressed Scalable Vector Graphics (RSVG 2.40.13)
```

If this is not the case your version is not compiled with librsvg, then you get the following.
```
      SVG  SVG       rw+   Scalable Vector Graphics (XML 2.9.4)
     SVGZ  SVG       rw+   Compressed Scalable Vector Graphics (XML 2.9.4)
```

Follow the steps to fix this issue:

`$ sudo apt purge imagemagick`

```bash
$ cd /tmp
# check for new releases: https://github.com/ImageMagick/ImageMagick6/releases
$ wget https://github.com/ImageMagick/ImageMagick6/archive/6.9.11-19.tar.gz
$ tar -xvf 6.9.10-24.tar.gz
$ cd ImageMagick6-6.9.10-24
$ ./configure --with-rsvg
$ make
$ sudo make install
```

Set the correct path: `$ sudo ln -s /usr/local/bin/convert /usr/bin/convert`  
If you get an error here that this file already exists, please execute `$ sudo apt autoremove`

Now `convert -list format` reports

      SVG  rw+   Scalable Vector Graphics (RSVG 2.40.16)
     SVGZ  rw+   Compressed Scalable Vector Graphics (RSVG 2.40.16)

Restart Invidious, just to be sure `$ sudo systemctl restart invidious.service`