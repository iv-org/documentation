# Frequently Asked Questions

## Table of Contents

- Using invidious
  * [Can I use Invidious on my device?](#q-can-i-use-invidious-on-my-device)
  * [Do you plan to make an Android/iOS app?](#q-do-you-plan-to-make-an-androidios-app)

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


# Commonly encountered errors

## **Q:** The media could not be loaded…

**A:** This problem can occur in different scenarios:

* If you're trying to watch a music clip, Youtube is likely blocking the
  video stream. Try enabling `proxy videos` in the preferences (or add
  `&local=1` in the URL). Switching instance is also a good alternative,
  as this type of content is often geo-restricted.

* Youtube often sends corrupted video data for the `hd720`, `medium` and
  `small` quality settings. Refreshing the page multiple times (5-7) can
  fix the problem. You may also set your `preferred video quality` to
  `dash` (or add `&quality=dash` to the URL).

* Rarely, it can be due to an internal failure of the instance and the
  video stream can't be fetched. A simple page refresh can solve the issue.

If none of the solutions listed above fix that problem, try switching
instances. And if that still doesn't work, you'll have to watch the video
on youtube itself (sorry for the inconvenience).

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
