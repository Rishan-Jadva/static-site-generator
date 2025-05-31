# HTB - GreenHorn

Target IP - 10.10.11.25

## Enumeration

#### Open Ports

- Port 22 - SSH
- Port 80 - HTTP
- Port 3000 - ppp?

#### Nmap

![[Pasted image 20241215230400.png]]

## Website

We first need to add greenhorn.htb to our /etc/hosts.
Then we are presented with:

![[Pasted image 20241215230525.png]]

We also are able to identify that the CMS for this application is pluck, by clicking on admin at the bottom of the page we are greeted with an admin login page which tells us the version of the application.

![[Pasted image 20241215230758.png]]

By also opening the http page on port 3000, we see a Gitea instance, which seems to contain the source code for the application:

![[Pasted image 20241215231358.png]]

By looking through all the files, we see the location of the password:

![[Pasted image 20241215231442.png]]

By analysing this hash in hash analyser, we see that this is a sha2-512 hash:

![[Pasted image 20241215231923.png]]

Then using crackstation, we can crack the hash and receive the password for the user:

![[Pasted image 20241215232049.png]]

## Exploit

Logging in we see the admin page for the pluck CMS application:

![[Pasted image 20241216001841.png]]

We see we can upload a module here:

![[Pasted image 20241216002015.png]]

We will upload a php reverse shell to the website and then receive the webshell, attempting to get a reverse shell by uploading a .php file does not work, this is because modules must be in a zip format or similar.

![[Pasted image 20241216002125.png]]

After successfully uploading the zip file, we will move to the directory that contains the module under the endpoint /data/modules/(zip_name)/(reverse-shell_name). Before moving to the endpoint, make sure the netcat listener is active.

![[Pasted image 20241216002808.png]]

We will now upgrade out shell to bash and make it interactive.

![[Pasted image 20241216003657.png]]

## Privilege Escalation

Heading to home files, we see that there is a user junior, we can attempt to reuse the password that we used to login to the pluck web application here, incase they reuse the password.

![[Pasted image 20241216003837.png]]

Success now we are able to read user.txt:

![[Pasted image 20241216003906.png]]

Additionally, Junior's home directory also includes a pdf file that has instruction on how to use OpenVAS. Opening the file we see:

![[Pasted image 20241216004816.png]]

Looking at the password, we have a pixelated obfuscated password, by searching online we find a Depix software here: https://github.com/spipm/Depix.git

After running the software we obtain this image:

![[Pasted image 20241216010136.png]]

After attempting to upgrade to root, we see that the password is correct:

![[Pasted image 20241216010442.png]]

Thereafter, heading to root's home we receive this root.txt:

![[Pasted image 20241216010516.png]]


