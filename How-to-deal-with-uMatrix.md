---
title: How-to-deal-with-uMatrix
description: 
published: true
date: 2021-05-23T16:58:41.524Z
tags: 
editor: markdown
dateCreated: 2021-01-28T20:39:36.844Z
---

If you're using [uMatrix](https://github.com/gorhill/uMatrix), you won't be able to automatically play a video served by Invidious on other websites without unblocking requests to Invidious instances.

So, to make it work, you'll need to allow `css`, `image`, `media`, `script`, `xhr`, `frame` for the instance from which you're trying to play the video.

Since there are many Invidious instances, you can use the tool called [Invimatrix](https://booteille.gitlab.io/invimatrix) to automatically generate uMatrix rules for every known instance.
