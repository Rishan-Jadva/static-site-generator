# THM - The Sticker Shop

Target IP - 10.10.10.60

## Enumeration

#### Open Ports

- Port 22 - SSH
- Port 8080 - HTTP

#### Nmap

![[Pasted image 20241130020824.png]]

## Website

We seem to have a simple website about a cat sticker shop. However, there does not seem to be much on this website even including the source code.

![[Pasted image 20241130021023.png]]

There seems to be not much of anything on this page however, looking at the feedback page, there may be a Cross Site Scripting (XSS) vulnerability. 

![[Pasted image 20241130022201.png]]

Trying the payload:
```
<script>alert("Hi")</script>
```

We don't get anything, which means either there is nothing going on or there is a blind xss vulnerability.

