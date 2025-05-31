# THM - Whiterose

Target IP - 10.10.102.155

## Enumeration

#### Open Ports

- Port 22 - SSH
- Port 80 - HTTP

#### Nmap Scan

![[Pasted image 20241201185332.png]]

## Website

Add cyprusbank.thm to /etc/hosts.
We see a website that is under maintenance which does not have anything hidden that we can see.

![[Pasted image 20241201185141.png]]

#### Gobuster

Does not seem to be anything yet but we will check back on it.

![[Pasted image 20241201185715.png]]

#### ffuf

Using ffuf we will enumerate the possible subdomains of the website.

![[Pasted image 20241201190536.png]]

Here we have found the admin subdomain. We will add it to our /etc/hosts then check website at that subdomain.

![[Pasted image 20241201190723.png]]

Now we have found a login page, we can use the credentials that we were given and login to this page.

![[Pasted image 20241201190850.png]]

Now we are given a list of transactions with different peoples names and balances.
Moving through the directories we come across an admin chat, there may be an Insecure Direct Object Reference (IDOR) Vulnerability because of the url being structured like this:

![[Pasted image 20241201191616.png]]

By changing the value from 5 to 0 we are able to find some secret chats containing a password for another user Gayle:

![[Pasted image 20241201191743.png]]

We will first try and login as Gayle through the website before we try logging in using SSH:

![[Pasted image 20241201191930.png]]

Now we are able to login and see all the private credentials of all the users as well as access the settings that we couldn't as user olivia:

![[Pasted image 20241201192022.png]]

In the settings page we find that we are able to change the password for any user. By testing it out with some data we see that there might be a cross-site scripting (XSS) vulnerability:

![[Pasted image 20241201192227.png]]

It seems to use the user input to output text onto the screen. We will test for any vulnerabilities by capturing the request in BurpSuite.
By removing the password from the POST request, we seem to find an error and it also gives us some files that we can search for vulnerabilities for:

![[Pasted image 20241201193046.png]]

Here we have found ejs, by looking up ejs vulnerabilities we find that there seems to be a Server-Side Template Injection (SSTI) vulnerability for ejs. By looking at the PoC's and exploits we are able to use them to attempt to exploit the web application.

![[Pasted image 20241201194106.png]]

Now we were able to receive a web shell:

![[Pasted image 20241201194146.png]]

We will check what sudo commands we can run as web:

![[Pasted image 20241201194758.png]]

Checking the version of sudoedit and searching online for vulnerabilities we find that there it is a vulnerable version that can lead to privilege escalation under CVE-2023-22809:

![[Pasted image 20241201202609.png]]
