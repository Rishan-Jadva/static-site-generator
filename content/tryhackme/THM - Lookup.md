# THM - Lookup

## Enumeration

#### Open Ports

- Port 22 - SSH
- Port 80 - HTTP

#### Nmap

![[Pasted image 20241129155115.png]]

#### Gobuster

After running a gobuster scan, there seems to be no directories directly accessible.

## Website

Had to add lookup.thm to /etc/hosts.

![[Pasted image 20241129155428.png]]

There seems to be a login page and upon attempting to login using some random details, it seems to send that request to a login.php page to log in.

We will now use ffuf to attempt to bruteforce the login page. 
Given that we know the there is a different page when using the user admin we will just try to find the password for the admin user.

![[Pasted image 20241129164812.png]]

Here we found the password123 that produced different results however when we place that in the login form, it shows the original error as if the user was incorrect.
Let's try and use the password but for a different user.

![[Pasted image 20241129165358.png]]

Here we have found the user jose with the password password123.
Logging into the application we have found a new files.lookup.thm subdomain that we have to put in /etc/hosts.

![[Pasted image 20241129165945.png]]

Looking for information about the software we see:

![[Pasted image 20241129170011.png]]

Looking up vulnerabilities for this software we find CVE-2019-9194 which is a Command Injection vulnerability. Using the exploit I found we receive a shell:

![[Pasted image 20241129171104.png]]

However, this shell is not functional so we will need to make a reverse shell, going to reverse shell generator we get a reverse shell on our device.

![[Pasted image 20241129171605.png]]

![[Pasted image 20241129171614.png]]

We will then upgrade the shell:

![[Pasted image 20241129171845.png]]

## Privilege Escalation

We will upload LinPEAS to find vulnerabilities to escalate privilege.

![[Pasted image 20241129172848.png]]

We see a setuid, we have made a vulnerability to make the path that the pwm uses to use id to give use the .passwords of the think user. 

![[Pasted image 20241129174621.png]]

Then using hydra we were able to find the correct password given this list:

![[Pasted image 20241129174658.png]]

We then login as the think use using the correct password.
Then we search for commands we can run as sudo on think.

![[Pasted image 20241129174813.png]]

Heading to GTFObins we find that look binary has an exploit. We will use that to escalate the privilege to root.
According to GTFObins we are able to read any file we want as root. So what if we read the ssh id_rsa for root.

![[Pasted image 20241129175956.png]]

Login to ssh as root:

![[Pasted image 20241129180041.png]]

