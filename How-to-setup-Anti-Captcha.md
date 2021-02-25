---
title: How-to-setup-Anti-Captcha
description: 
published: true
date: 2021-02-25T18:05:05.107Z
tags: 
editor: undefined
dateCreated: 2021-01-28T20:39:41.544Z
---

1. Register on anti-captcha.com: https://anti-captcha.com/clients/entrance/register and finish the registration with the link provided in your mailbox.
2. Head over the "Add fund" page: https://anti-captcha.com/clients/finance/refill and use whatever currency you prefer to use for adding $2 into your balance.   
Do note that cryptocurrencies give a bonus of 20% at the first time you add funds then 10% for each new recharge.
3. After adding funds, go the API key link: https://anti-captcha.com/clients/settings/apisetup and copy your "Account key" (**never share it, it's confidential**).
4. Edit your Invidious `config.yml` file (should be located in the `config` directory) and add your account key at the end of the file after the `captcha_key` parameter.   
Here is an example:   
```yml
captcha_key: acuGae2riad5quashoug3Leeh
```
5. Restart Invidious and that's it!