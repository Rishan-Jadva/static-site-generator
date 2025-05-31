# HTB - Validation

## Enumeration

#### Open Ports

- Port 22 - SSH
- Port 80 - HTTP
- Port 4566 - HTTP
- Port 8080 - HTTP

#### Nmap Scan

![[Pasted image 20241202053603.png]]

## Website

In this website we see a registration page, within it we find a quick Cross-Site Scripting vulnerability by executing an alert in the username section.

![[Pasted image 20241202055056.png]]

![[Pasted image 20241202055433.png]]

We see that there is a vulnerability however, from there, I cannot seem to find another way to get any credentials. So maybe we check the post request in BurpSuite, to try and find if there is also a SQL Injection (SQLi) vulnerability:

![[Pasted image 20241202060240.png]]

By adding an apostrophe to the end of the country variable, we are able to receive a SQL error:

![[Pasted image 20241202060501.png]]

So now we are able to execute a FILE OUT attack, where we are able to add a file to the website to execute commands. By executing this:

![[Pasted image 20241202062300.png]]

we are able to go to the shell.php page with a parameter to execute a command, there we can add the reverse bash shell that is url encoded to the end of the link to execute the shell which will connect to our system and now we have a shell as www-data on the system:

![[Pasted image 20241202062430.png]]

## Privilege Escalation

Now we will check all the config files to see if a password or username is shown.

![[Pasted image 20241202062925.png]]

There is a password located in config.php. Maybe we can use this password to login as root:

![[Pasted image 20241202063047.png]]

And we successfully have root on the target system, now we can find the root.txt.
