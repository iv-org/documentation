# How to setup Anti-Captcha

1. [Register on anti-captcha.com](https://anti-captcha.com/clients/entrance/register) and finish the registration with the link provided in your mailbox.
2. Head over to the [Add fund](https://anti-captcha.com/clients/finance/refill) page and use whatever currency you prefer to use for adding $2 into your balance.
Do note that cryptocurrencies give a bonus of 20% the first time you add funds and then 10% for each new recharge.
3. After adding funds, go to the [API key link](https://anti-captcha.com/clients/settings/apisetup) and copy your `Account Key` (**never share it, it's confidential**).
4. Edit your Invidious `config.yml` file (should be located in the `config` directory) and add your account key at the end of the file after the `captcha_key` parameter.
Here is an example:
```yml
captcha_key: acuGae2riad5quashoug3Leeh
```
5. Restart Invidious and that's it!
