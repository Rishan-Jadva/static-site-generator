# (Day 14) - Advent of Cyber

## Certificate Mismanagement

#### Setup

Add the following host to our /etc/hosts file:

```
echo "10.10.105.65 gift-scheduler.thm" >> /etc/hosts
```

To ensure that the host is in our file we can run the following command which should give a similar output:

```
cat /etc/hosts

127.0.0.1       localhost
127.0.1.1       RJ-Laptop.      RJ-Laptop

192.168.1.11    host.docker.internal
192.168.1.11    gateway.docker.internal
127.0.0.1       kubernetes.docker.internal

::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

10.10.105.65 gift-scheduler.thm
```

Now we will open up the domain in a browser under the following link:
`https://gift-scheduler.thm`

We will click to view the certificate, the browser indicates that the certificate is self-signed and not secure. So by viewing the certificate we identify that the issuer was THM.

Now by continuing to the website we see this:

![[Pasted image 20241229182530.png]]

We can login using the provided credentials and now we see this application:

![[Pasted image 20241229182707.png]]

#### Burpsuite

Due to the fact that the certificate is self-signed we can intercept requests. To do this we will first open up Burpsuite to capture the traffic. We will turn on intercept and then go to the proxy settings and set a listener on our IP address.

Now we will update the /etc/hosts file with our IP address with the Wareville Gateway:

```
echo "10.4.109.132 wareville-gw" >> /etc/hosts
```

We will now run the route-elf-traffic.sh script to capture requests.
Now heading into Burpsuite and heading towards HTTP History we see the following requests.

![[Pasted image 20241229183917.png]]

![[Pasted image 20241229183934.png]]

![[Pasted image 20241229184024.png]]

![[Pasted image 20241229184049.png]]

![[Pasted image 20241229184107.png]]

![[Pasted image 20241229184122.png]]

Now we are able to use the following POST requests and login to their respective accounts.
We will login as snowballelf:

![[Pasted image 20241229184514.png]]

There we see one of the flags.

We will now login to marta_mayware's account:

![[Pasted image 20241229184720.png]]

There we obtain another flag.

