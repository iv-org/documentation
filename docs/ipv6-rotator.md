# Rotate your IPv6 address for escaping YouTube blocking

This tutorial has been written by [unixfox](https://github.com/unixfox), owner of [yewtu.be](https://yewtu.be/). He is better suited when looking for help about this tutorial.

## Synopsis

YouTube has started to periodically block the public Invidious instances since the start of June 2023 ([iv-org/invidious/issues/3872](https://github.com/iv-org/invidious/issues/3872)) and they have become more aggressive about it since the start of August 2023 ([iv-org/invidious/issues/4045](https://github.com/iv-org/invidious/issues/4045)).

Due to this block, "local proxy" and DASH do not work anymore. But Invidious still works for most videos without using the proxy, because the video playback traffic is sent directly to YouTube servers without going through the instance.

Thanks to IPv6 you can easily escape this block because there are many IP addresses in a single /64 IPv6 range. (18,446,744,073,709,551,616 IP addresses to be precise)

This tutorial will explain how to automatically and periodically rotate your IPv6 address. Also some notes about how to have IPv6 in case your provider does not offer it.

## Requirements
#### 1) IPv6 support on your server
##### Testing
You can easily find out if you have IPv6 by executing the command:
```
curl -m 5 ipv6.icanhazip.com
```     
If you do not have any errors, then congratulation, you can continue to [the second requirement](#2-system-packages-requirement)!

If you do have an error (timeout or no route to host), then you will need to enable IPv6 support on your server.  
Depending on your provider and if it does support IPv6, you may have to configure your server for IPv6. Check the documentation of your provider.

##### Other solutions if you do not have IPv6 support

###### 1) Switch to another provider

If your provider does not support IPv6 then you can either switch to another provider that support IPv6.  
There are many today that do support it, here is a non-exhaustive list of them (**this is not recommendation, just a list of the popular providers that support IPv6**):  
Hetzner, BuyVM, Scaleway, OVH, DigitalOcean, Vultr, Incognet, Netcup and more.   
Larger list: https://www.serverhunter.com/#query=ips%3Aipv6   

###### 2) Use an IPv6 tunnelbroker or make one yourself

The alternative, if you do not want to switch provider, is to use an IPv6 tunnelbroker. It allows to get IPv6 connectivity using another server.

This website lists all the free and paid existing tunnelbrokers: https://tunnelbroker.services/. **We do not recommend running a public instance on a free tunnelbroker as this would put a lot of strain on their network because video streaming consumes a lot of bandwidth.**  

You can also use an external server (from another provider that do support IPv6) for acting as an IPV6 tunnel for your main server. Wireguard is perfectly suited for that.  
All of this is out of scope of this tutorial, please consult the internet for tutorials.

#### 2) System packages requirement
Please install:

- python requests library.  
  Debian/Ubuntu: `sudo apt install python3-requests`  
  RHEL/CentOS/Fedora: `sudo dnf install python-requests`    
  Other Linux distributions: `sudo yourpackagemanager install python-requests`
- python pyroute2 library.   
  Debian/Ubuntu: `sudo apt install python3-pyroute2`   
  RHEL/CentOS/Fedora: `sudo dnf install python-pyroute2`  
  Other Linux distributions: `sudo yourpackagemanager install python-pyroute2`

## Configure Invidious for IPv6
### If you are running Invidious outside of Docker or using something else than Docker (K8s)

Please make sure that you have this line set in `config.yml`:

```yaml
force_resolve: ipv6
```

Note: If you are on Kubernetes, check that your pods have IPv6 connectivity. But you probably already know that if you are using Kubernetes.

### If you are running Invidious in Docker
Note: Make sure you are running a recent version of Docker if you are running into IPv6 issues.

If needed, IPv6 official documentation for Docker is at https://docs.docker.com/config/daemon/ipv6/.

1. Put the following config in `/etc/docker/daemon.json`:
   ```
   {
    "experimental": true,
    "ip6tables": true
   }
   ```
2. Restart Docker
3. In your docker-compose file of Invidious. Add these lines at the end of your docker-compose
   ```yaml
   networks:
     default:
       enable_ipv6: true
       ipam:
         config:
           - subnet: 2001:0DB9::/112
             gateway: 2001:0DB9::1
   ```
   Note: Don't change the subnet and the gateway. Unless there is a conflict with an existing docker network.
4. Make sure that you have this line set in `config.yml`:
   ```yaml
   force_resolve: ipv6
   ```
5. Bring down your docker composition and bring it back up for recreating the network:
   ```
   docker compose down
   docker compose up -d
   ```
6. To check if everything went well then do:
   ```
   docker compose exec invidious ping -c 1 ipv6.icanhazip.com
   ```
   If you do not get any error then you can jump to the next step.

## Configure the IPv6 rotator (made by Invidious team)
This tool was developed by the Invidious team, and it's the official tool for rotating your IPv6 address on Invidious: https://github.com/iv-org/smart-ipv6-rotator.  
It may be used on other projects that depend on YouTube and/or Google (example: Piped or SearXNG).

1. Make sure you have installed all the python libraries from [the "requirements"](#requirements).
2. Clone the repository somewhere that you like (not inside the invidious directory):
   ```
   git clone https://github.com/iv-org/smart-ipv6-rotator.git
   ```
3. Find the IPv6 subnet of your server, usually it's written on your provider website.  
   But you can easily find it using this tool: http://www.gestioip.net/cgi-bin/subnet_calculator.cgi.  
   Enter the main IPv6 address, select IPv6 and change the prefix length only if it's not a /64.  
   Use the command `ip a` to get the detail of your IPv6 network configuration.
4. Run the script once like this (don't use sudo if you are already root):
   ```
   sudo python smart-ipv6-rotator.py run --ipv6range=YOURIPV6SUBNET/64
   ```
5. If everything went well, then configure a cron to periodically rotate your IPv6 range. Twice a day (noon and midnight) is enough for YouTube servers. Also at the reboot of the server!
   Example crontab (`crontab -e -u root`):
   ```
   @reboot sleep 30s && python /path/to/the/script/smart-ipv6-rotator.py run --ipv6range=YOURIPV6SUBNET/64
   0 */12 * * * python /path/to/the/script/smart-ipv6-rotator.py run --ipv6range=YOURIPV6SUBNET/64
   ```  
   The `sleep` command is used in case your network takes too much time to be ready.

That's it!

If the script does not work for you, it could be that:

- Your provider does not allow you to assign any arbitrary IPv6 address, it's common for cloud providers like AWS, Oracle Cloud, Google Cloud where you need to manually assign the IPv6 address from the panel.
- You have not correctly set your IPv6 subnet range. In such case, please ask for help on IRC or Matrix or in a GitHub issue.

If you find any other issues, please open a bug report there: https://github.com/iv-org/smart-ipv6-rotator/issues
