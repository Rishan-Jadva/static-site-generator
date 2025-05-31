# HTB - Analytics

Target IP - 10.10.11.233

## Enumeration - 

### threader3000

![[Pasted image 20241127093610.png]]

### Nmap

![[Pasted image 20241127093728.png]]

### Taking a look at the website

![[Pasted image 20241127094002.png]]

Add analytical.htb to /etc/hosts
Upon further enumeration of the site. The login page redirects to data.analytical.htb which will also have to be placed in /etc/hosts.

#### Login Page

![[Pasted image 20241127094727.png]]

Here we find the login of the application running using Metabase version v0.46.6.

## Exploitation

Upon figuring out the version of Metabase, through a quick google search, we find a Pre-Authentication Remote Code Execution vulnerability with CVE-2023-38646.

Here we find a github Proof of Concept: https://github.com/Red4mber/CVE-2023-38646/blob/main/README.md
Upon exploiting the target, I am able to get a shell as metabase.

## Privilege Escalation

We need to check the environment variables. In this we find credentials in the META_USER and META_PASS variables. We are then able to get a shell using ssh.

Then by finding out the version of ubuntu we are running. We discover another CVE for this distribution. By running a PoC of the version we are able to gain root.