#### Warning: If you use imagemagick on Ubuntu for other services like Mastodon this guide may breaks them, please use [this guide](https://linuxconfig.org/how-to-install-imagemagick-7-on-ubuntu-18-04-linux) instead.
There is some issue on Debian 9 and Ubuntu 18.04 and later. It appears that the clock (the captcha) has no hands but you can see them outside the clock. You need to compile imagemagick yourself with rsvg to solve this issue.  
Thanks [Tmiland](https://github.com/tmiland) for showing up a solution at [#299](https://github.com/omarroth/invidious/issues/299)

You can check if your version of imagemagick is affected with `convert -list format`.  
It should show the following if your installed version is okay.
```
      SVG  SVG       rw+   Scalable Vector Graphics (RSVG 2.40.13)
     SVGZ  SVG       rw+   Compressed Scalable Vector Graphics (RSVG 2.40.13)
```

If this is not the case your version is not compiled with rsvg, then you get the following.
```
      SVG  SVG       rw+   Scalable Vector Graphics (XML 2.9.4)
     SVGZ  SVG       rw+   Compressed Scalable Vector Graphics (XML 2.9.4)
```

Follow the steps to fix this issue:

`$ sudo apt purge imagemagick`

```bash
$ cd /tmp
# check for new releases: https://github.com/ImageMagick/ImageMagick6/releases
$ wget https://github.com/ImageMagick/ImageMagick6/archive/6.9.10-24.tar.gz
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