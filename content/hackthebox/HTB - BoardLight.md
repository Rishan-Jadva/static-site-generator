# HTB - BoardLight

### Enumeration

#### Open Ports

- TCP Port 22 - SSH
- TCP Port 80 - HTTP

#### Nmap Scan

![[Pasted image 20241128193813.png]]

##### Sub-domain Scanning

Using ffuf we are able to find subdomains for the domain.

![[Pasted image 20241128200729.png]]

Here we find the crm subdomain. We need to add it to /etc/hosts for it to work.

When we got to the subdomain we find a CMS login page.

![[Pasted image 20241128200921.png]]

Searching online we find CVE-2023-30253 for this specific application and version.
Using this exploit we get a reverse shell.

![[Pasted image 20241128201332.png]]

![[Pasted image 20241128201343.png]]

Moving around we find a config file that shows a password serverfun2$2023!!.
Then by using su we are able to change user to larissa using this password.

![[Pasted image 20241128201821.png]]

###### User.txt 84a20215625069f3ee162205c6028422

### Privilege Escalation

Now that we are larissa by checking id we see that we are of adm group. 

![[Pasted image 20241128202731.png]]

By running find / -perm /4000 2>/dev/null we find that there are some suid binaries that are usually not there on other systems. These binaries relate to the enlightenment program.

![[Pasted image 20241128202917.png]]

Next to find the version of enlightenment we use /etc/enlightenment --version

![[Pasted image 20241128203005.png]]

Here we find the version 0.23.1. By searching online, we find that enlightenment has an exploit under CVE-2022-37706. We download the script to the attacker machine and then receive the script using wget.

![[Pasted image 20241128203411.png]]

![[Pasted image 20241128203432.png]]

Now we need to run the exploit using /bin/bash because we cannot run scripts with this user.

![[Pasted image 20241128203351.png]]

Now we have root and are able to get root.txt.

###### Root.txt 931821a1ce2510e1f72ca657cc95228a
