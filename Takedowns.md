---
title: DMCA
description: 
published: true
date: 2021-11-16T16:58:51.441Z
tags: 
editor: markdown
dateCreated: 2021-11-16T16:58:48.431Z
---

While running Invidious, it is very possible you will recive a DMCA at some point. A copyright agent will probably at some point search the ID of an infringing video on a search engine and see an Invidious instance appear. At least in the United States, Invidious instances should in theory be immune to DMCA laws because of [17 U.S. Code § 512](https://www.law.cornell.edu/uscode/text/17/512) stating that a provider is not responsible for content assusimg that "the material is transmitted through the system or network without modification of its content."

## Sample DMCA (United States)

```
Hello,

I am writing on behalf of {{website}}. I am the webmaster of {{website}} and all of its subdomains.

I see you are filing a claim for {{invidious instance url}}. {{invidious instance url}} hosts Invidious, a private YouTube front-end, meaning it is simply a proxy to access YouTube assets and user generated content without tracking from Google. Thus, all content is proxied from YouTube and is not stored on our servers and if YouTube chooses to remove an asset, it will no longer appear on our site.
Under United States copyright law 17 U.S.C. § 512(a), part of the Digital Millennium Copyright Act, we cannot be liable for content that "is transmitted through the system or network without modification of its content." It should be noted our {{server hosting}} {{invidious instance url}} is hosted in the United States.

In the meantime, while we cannot control the content on YouTube that our site proxies, we recommend that you send a claim to YouTube.

Thank you,
{{name}}
```

## Sample Template (EU)

```
Hello,

I am writing on behalf of {{website}}. I am the webmaster of {{website}} and all of its subdomains.

I see you are filing a claim for {{invidious instance url}}. {{invidious instance url}} hosts Invidious, a private YouTube front-end, meaning it is simply a proxy to access YouTube assets and user generated content without tracking from Google. Thus, all content is proxied from YouTube and is not stored on our servers and if YouTube chooses to remove an asset, it will no longer appear on our site.
Under the directive 2001/29/EC of the European Parliament and of the Council of 22 May 2001 on the harmonisation of certain aspects of copyright and related rights in the information society, "temporary acts of reproduction referred to in Article 2, which are transient or incidental [and] an integral and essential part of a technological process and whose sole purpose is to enable: a transmission in a network between third parties by an intermediary" https://wipolex.wipo.int/en/text/126977 is allowed. It should be noted our {{server hosting}} {{invidious instance url}} is hosted in the European Union.

In the meantime, while we cannot control the content on YouTube that our site proxies, we recommend that you send a claim to YouTube.

Thank you,
{{name}}
```
