# HTB - Busqueda

Target IP - 10.10.11.208

## Enumeration

#### Open Ports

- Port 22 - SSH
- Port 80 - HTTP

#### Nmap

![[Pasted image 20241129212539.png]]

## Website

First I need to add the website to /etc/hosts.
Now we should be able to access the website.

![[Pasted image 20241129212726.png]]

After seeing this page I saw a software with a version number:

![[Pasted image 20241129212842.png]]

After looking online it seems that this software is vulnerable to Arbitrary CMD Injection under CVE-2023-43364.
Now I will run the exploit and we should be able to obtain a reverse shell.

![[Pasted image 20241129213321.png]]

![[Pasted image 20241129213333.png]]

Now we will upgrade the shell.

![[Pasted image 20241129213551.png]]

After obtaining a shell as svc we are able to obtain the user.txt.

## Privilege Escalation

We will being with uploading linPEAS to the target machine to determine any location that can be used for privilege escalation.

Looking through we find an interesting file in the web app '.git'. Heading into the config file we find a link in relation to another application with credentials for the cody user which seems to also be the svc user. So now we can ssh into svc using these credentials and get a more stable shell.

![[Pasted image 20241130010854.png]]

Heading to the website and logging in as cody, we find this application:

![[Pasted image 20241130011130.png]]

Checking the version number, there is no known exploits, so we will try to find something within this application that we can use to escalate our privileges.

After trying to find some bad commit or anything, there seems to be nothing except for the ability to login as administrator if I can find the password elsewhere.

Let's move back to the ssh session, I found that the user svc can run a command as root:

![[Pasted image 20241130011911.png]]

Moving to this python script we find out that we cannot read or edit this file:

![[Pasted image 20241130012146.png]]

However, let's try and execute this script and see if we are able to exploit it:

![[Pasted image 20241130012413.png]]

It looks like we can find out about the docker containers by running the command with docker-ps:

![[Pasted image 20241130012549.png]]

The commands that we are able to run seem similar to commands you can run on a regular docker container. So in terms of format, if we see the types of formats that docker accepts for the docker-inspect command.

We see that we are able to use the format '{{json .}}'.
Then by piping this output to jq we are able to read the json file for the container much easier:

![[Pasted image 20241130013844.png]]

Here we find that there is an exposed password, trying to get root using this password does not work, so how about we try and login to the gitea web application as the administrator using this password.

![[Pasted image 20241130014401.png]]

Here we find a set of scripts that we were running as root on the machine. Let's look into each file to try and find an exploit.

Looking at the code for the system-checkup.py we find that the other command we couldn't run full-checkup. We see in this script, the full-checkup file that we want to run is a relative path so we may be able to write our own exploit:

![[Pasted image 20241130014856.png]]

Before when we ran the script, the script would not work because it could not find the full-checkup.sh script but now that we are in /opt/scripts it runs fine:

![[Pasted image 20241130015146.png]]

This means that we can write a script in the home directory and execute a reverse shell:

![[Pasted image 20241130015816.png]]

Now we are able to get root.txt.