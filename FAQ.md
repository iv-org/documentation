# Frequently Asked Questions

## Table of Contents

- Using invidious
  * [Can I use Invidious on my device?](#q-can-i-use-invidious-on-my-device)
  * [Do you plan to make an Android/iOS app?](#q-do-you-plan-to-make-an-androidios-app)
  * [What data is collected by Invidious?](#q-what-data-is-collected-by-invidious)
  * [What data is shared with YouTube?](#q-what-data-is-shared-with-youtube)

- Commonly encountered errors
  * [The media could not be loaded…](#q-the-media-could-not-be-loaded)
  * [Could not check out a connection in 2.0 seconds (DB::PoolTimeout)](
    #q-could-not-check-out-a-connection-in-20-seconds-dbpooltimeout)

- Running your own instance
  * [Do you provide pre-built binaries (`.deb`, `.rpm`, etc..)?](
    #q-do-you-provide-pre-built-binaries-deb-rpm-etc)
  * [How can I configure _[thing]_?](#q-how-can-i-configure-thing)
  * [RSS feeds/links/etc... URLs redirect to `<IP>:3000` but I have a reverse proxy!](
    #q-rss-feedslinksetc-urls-redirect-to-ip3000-but-i-have-a-reverse-proxy)
  * [The "popular" feed/page on my instance is empty!](
    #q-the-popular-feedpage-on-my-instance-is-empty)


# Using invidious

## **Q:** Can I use Invidious on my device?

**A:** As long as your device is equipped with a modern web browser,
sure, of course! A responsive interface is available for mobile/tablets.

<br/>

## **Q:** Do you plan to make an Android/iOS app?

**A:** No. Invidious is and will always be a browser application.

If you have an Android phone/tablet, you can check the
[NewPipe](https://github.com/TeamNewPipe/NewPipe/) application.

<br/>

## **Q:** What data is collected by Invidious?

**A:** Invidious by itself does not collect any data about its users, but
keep in mind that instance owners can log your IP address (like any other
server on the internet).

By default, the server logs which URLs were accessed, the associated error
code (e.g 404 if the URL was not found) and the time it took for the server
to respond.

Here is what the server logs looks like:

```
2021-08-30 18:15:44 UTC [info] 200 GET /watch?v=GIAKHj9uJtM 781.21ms
2021-08-30 18:15:49 UTC [info] 200 GET /api/v1/search?q=Fly%20away 500.0ms
2021-08-30 18:15:49 UTC [info] 200 GET /vi/lJcqAzWFWLs/mqdefault.jpg 15.82ms
2021-08-30 18:15:49 UTC [info] 200 GET /vi/JoP_Tte7z7o/mqdefault.jpg 70.64ms
```

When you create an account, your watch history and the list of channels you
subscribed will be stored in the server's database. You can export, migrate
or delete these data at any time from your user account page.

<br/>

## **Q:** What data is shared with youTube?

**A:** By default, the video stream is fetched directly from Google's servers
(`googlevideo.com`) in order to reduce the bandwidth required by invidious,
meaning that Google will be able to see your IP address and some other data
commonly sent by web browsers, like your user-agent string.

If you don't want that to happen, you can go to the `preferences` page and
check the `Proxy videos` option. When this option is enabled, the invidious
instance will be used as a relay (also know as a "proxy") between you and
Google's servers, which will hide your IP address and the other information
sent by your browser.

<br/>


# Commonly encountered errors

## **Q:** The media could not be loaded…

**A:** This problem can occur when Youtube sends corrupted video data.
Try switching instance. Reloading the page a few times may also help.

_Note:_ If you're trying to listen to music, you will have to go to Youtube.
This type of content is protected by DRM. We currently don't support those.

<br/>

## **Q:** Could not check out a connection in 2.0 seconds (DB::PoolTimeout)

**A: Please, do not open a bug report on github, we can't do anything!**

The instance you are using is having _database issues_. Please use another
instance from the [list of public instances](https://instances.invidious.io)

<br/>


# Running your own instance

## **Q:** Do you provide pre-built binaries (`.deb`, `.rpm`, etc.)?

**A:** We currently don't provide those, due to the rolling release nature
of Invidious. Get a fresh `clone` or `pull` the latest commits from `master`
instead.

<br/>

## **Q:** How can I configure _[thing]_?

**A:** Read the example config file (`config/config.example.yml`).
All the supported configuration options are documented there.

<br/>

## **Q:** RSS feeds/links/etc... URLs redirect to `<IP>:3000` but I have a reverse proxy!

**A:** Make sure that the following parameters are set accrodingly to your environment:
- `https_only`: if your instance is served over HTTPs
- `domain`: if you have a domain name that redirects to your instance
- `external_port`: if your instance is accessed from a different port than
  the listening one (e.g your instance listens on :3000, but is available on 
  :443 through a reverse proxy, set `external_port` to `443`)

<br/>

## **Q:** The "popular" feed/page on my instance is empty!

**A:** The "popular" feed is generated from the videos that are popular amongst
the users registered on your instance. If nobody has created an account on your
instance (e.g if registration is disabled) the popular feed will be empty.
