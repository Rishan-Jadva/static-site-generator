# THM - Rabbit Hole

Target IP - 10.10.81.174

## Enumeration

#### Open Ports

- Port 22 - SSH
- Port 80 - HTTP

#### Nmap Scan

![[Pasted image 20241202041516.png]]

## Website

Looking at the website, there is a register and login page:

![[Pasted image 20241202041550.png]]

Registering a new account and logging in, we find that we can see logs for the admin logging in.

![[Pasted image 20241202041952.png]]

While testing a Cross-Site Scripting (XSS) vulnerability using this payload in the username and password fields:
`<script>alert("Hello")</script>`
I discovered that when you login using the same credentials we are given:

![[Pasted image 20241202043453.png]]\

This indicates that there may be a SQL Injection vulnerability instead, so we could possibly register a new user with the payload to try and enumerate the database using SQL:

![[Pasted image 20241202045148.png]]

Here we see we are able to execute SQL commands, now we will check the users table:

![[Pasted image 20241202045405.png]]

Here we see the columns available are: id, username and pass.
Assuming that pass means passwords we should be able to obtain a username and password for this site.
Here we have a portions of what seems to be an MD5 hash:

![[Pasted image 20241202045610.png]]

![[Pasted image 20241202045737.png]]

We cannot seem to crack this hash so we will now try and locate the processlist because we see that the admin account is logging in regularly so we are able to run a large payload to see the admin user and password:

![[Pasted image 20241202052721.png]]

Now we are able to login to ssh as admin:

![[Pasted image 20241202052820.png]]
