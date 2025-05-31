# HTB - PermX

## Enumeration

#### Open Ports

- Port 22 - SSH
- Port 80 - HTTP

#### Nmap Scan

![[Pasted image 20241203190624.png]]

## Website

We first need to add permx.htb to /etc/hosts.
Now we will enumerate the subdomains of permx.htb using ffuf:

![[Pasted image 20241203191525.png]]

Here we have found the subdomain lms.permx.htb after adding it to /etc/hosts we see:

![[Pasted image 20241203191737.png]]

This seems to be a login page, here we can see that the lms that is being run in chamilo, to get the version of chamilo that is being run we can move to the /README.md file. Within it we find that we are running version 1.11. Searching up online we see that this version is vulnerable to unauthenticated remote code execution. 

## Exploitation

![[Pasted image 20241203193007.png]]

We will now upgrade the shell using https://0xffsec.com/handbook/shells/full-tty/

![[Pasted image 20241203193408.png]]

## Privilege Escalation

We will use linPEAS to enumerate the machine and possibly achieve privilege escalation.

![[Pasted image 20241203194059.png]]

![[Pasted image 20241203194114.png]]

After running linPEAS we are able to find a database password:

![[Pasted image 20241203195133.png]]

Using this password we are able to escalate our privileges using ssh for the user mtz:

![[Pasted image 20241203195209.png]]

By running sudo -l, we are able to run /opt/acl.sh as root:

![[Pasted image 20241203195254.png]]

After reading and understanding the /opt/acl.sh file we understand that we need to create a symbolic link using ln -s:

![[Pasted image 20241203201751.png]]

