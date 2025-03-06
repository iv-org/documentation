# Invidious Instances

[Uptime History provided by updown.io](https://uptime.invidious.io)

[Instances API](https://api.invidious.io/)

**Warning: Any public instance that isn't in this list is considered untrustworthy. Use them at your own risk.**

**The list of public instances is short due to the [recent YouTube issues](https://github.com/iv-org/invidious/issues/4734). If you can, [please host Invidious at home](./installation.md) instead of using a public instance.**

## List of public Invidious Instances (sorted from oldest to newest):

* [inv.nadeko.net](https://inv.nadeko.net) 🇨🇱 - Source code/changes: https://git.nadeko.net/Fijxu/invidious - CAPTCHA: mCaptcha (https://mcaptcha.org/)

### Tor Onion Services:

* [inv.nadekonw7plitnjuawu6ytjsl7jlglk2t6pyq6eftptmiv3dvqndwvyd.onion](http://inv.nadekonw7plitnjuawu6ytjsl7jlglk2t6pyq6eftptmiv3dvqndwvyd.onion) 🇨🇱 (Onion of inv.nadeko.net)

### I2P Eepsites:

* [zzlsbhhfvwg3oh36tcvx4r7n6jrw7zibvyvfxqlodcwn3mfrvzuq.b32.i2p](http://zzlsbhhfvwg3oh36tcvx4r7n6jrw7zibvyvfxqlodcwn3mfrvzuq.b32.i2p) 🇨🇱 (Eepsite of inv.nadeko.net)

## Rules to have your instance in this list:

1. Instances MUST have been up for at least a month before it can be added to this list.
2. Instances MUST not be more than a month out of date compared with either the latest commit or latest release. Any instance that is more than a month out of date is considered unmaintained and will be removed from the list.
3. Instances MUST have statistics (`/api/v1/stats`) enabled (`statistics_enabled: true` in the configuration file).
4. Instances MUST have an uptime of at least 90% ([according to uptime.invidious.io](https://uptime.invidious.io/)).
5. Instances MUST be served via domain name.
6. Instances MUST be served via HTTPS (or/and onion).
7. Instances using any DDoS Protection / MITM MUST be marked as such (e.g. Cloudflare, DDoS-Guard).
8. Instances using any type of anti-bot protection MUST be marked as such.
9. Instances MUST NOT use any type of analytics, including external scripts of any kind.
10. Any system whose goal is to modify the content served to the user (i.e web server HTML rewrite) is considered the same as modifying the source code.
11. Instances running a modified source code:
    - MUST respect the [GNU AGPL](https://en.wikipedia.org/wiki/GNU_Affero_General_Public_License) by publishing their source code and stating their changes **before** they are added to the list
    - MUST publish any later modification in a timely manner
    - MUST contain a link to both the modified and original source code of Invidious in the footer.
12. Instances MUST NOT serve ads (sponsorship links in the banner are considered ads) NOR promote products.
13. Instances MUST NOT restrict or disallow the access / usage to any [natural person](https://en.wikipedia.org/wiki/Natural_person) (e.g. a country's IP range MUST NOT be blocked, access by a natural person MUST NOT be disallowed for arbitrary reason) - this rule doesn't apply to [juridical persons](https://en.wikipedia.org/wiki/Juridical_person).

**NOTE:** We reserve the right to decline any instance from being added to the list, and to remove / ban any instance breaking the aforementioned rules.
