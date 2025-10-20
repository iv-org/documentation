# Simple IPv6 rotation for avoid YouTube blocking (SLAAC)

## Requirements
- A host with IPv6 support providing a ``/64`` IPv6 prefix. (If your server provider provides smaller prefix lengths such as ``/128`` it is not sufficient for rotation)
- Docker with IPv6 networking enabled so that invidious can access the internet via IPv6

## Setup
### If the IPv6 address on your host is dynamically configured via Stateless Address Autoconfiguration (SLAAC)
Add the following to ``/etc/network/interfaces`` or equivalent configuration.

Note: The configuration syntax shown assumes use of ifupdown (/etc/network/interfaces). On systems using Netplan, systemd-networkd, or NetworkManager, IPv6 privacy extensions must be enabled via their respective configuration formats. 

This will enable the IPv6 privacy extensions which will allow the kernel to automatically generate new random IPv6 addresses which are temporary and stay assigned for the specified lifetime.
```
iface eth0 inet6 auto
    privext 2
    pre-up echo 2 > /proc/sys/net/ipv6/conf/eth0/use_tempaddr
    pre-up echo 3600 > /proc/sys/net/ipv6/conf/eth0/temp_valid_lft
    pre-up echo 1800 > /proc/sys/net/ipv6/conf/eth0/temp_prefered_lft
```
In this case the prefered lifetime is set to 30 minutes and the valid lifetime to 1 hour. Every 30 minutes a new temporary address will be assigned by the kernel.
The old address will be kept for 30 minutes longer (valid lifetime) for any remaining connections using it.


### If your IPv6 configuration is static

Run the below script every 30 minutes via a cronjob as root

``/usr/local/bin/ipv6-rotate.sh``
```
#!/bin/bash
# Set your network prefix (first 64 bits)
PREFIX="2001:db8:1234:5678"
INTERFACE="eth0"

# Generate random interface ID (last 64 bits)
INTERFACE_ID=$(printf "%04x:%04x:%04x:%04x" $((RANDOM % 65536)) $((RANDOM % 65536)) $((RANDOM % 65536)) $((RANDOM % 65536)))

#Enable prefering temporary addresses
echo 2 > /proc/sys/net/ipv6/conf/"$INTERFACE"/use_tempaddr

# Add the IPv6 address
ip -6 addr add "${PREFIX}":"${INTERFACE_ID}"/64 dev "$INTERFACE" valid_lft 3600 preferred_lft 1860
```
Replace the ``PREFIX`` and ``INTERFACE`` variables according to your setup. Note that if your IPv6 address is ``2001:db8:1234:5678::1``, the correct prefix is ``2001:db8:1234:5678``.

#### In the crontab:
```
*/30 * * * * /usr/local/bin/ipv6-rotate.sh
```
Don't forget to make it executable: ``chmod +x /usr/local/bin/ipv6-rotate.sh``


