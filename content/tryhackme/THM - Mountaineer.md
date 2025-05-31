# THM - Mountaineer

Target IP - 10.10.183.84

## Enumeration

#### Open Ports

- Port 22 - SSH
- Port 80 - HTTP

#### Nmap Scan

![[Pasted image 20241203164353.png]]

## Website

We are welcomed with a nginx server page. Due to the fact that nothing is present here, we will enumerate the rest of the pages with gobuster.

![[Pasted image 20241203164421.png]]

#### Gobuster

![[Pasted image 20241203164554.png]]

Here we find a /wordpress endpoint, by travelling to this domain we find a wordpress website.

![[Pasted image 20241203165048.png]]

We will now run gobuster again to see if we can enumerate any wordpress related enpoints:

![[Pasted image 20241203165605.png]]

There we find the admin page for wordpress and by attempting to login using the username admin, we find this message:

![[Pasted image 20241203165810.png]]

So now we can use hydra to attempt to crack the password for the site. 
However, after a long time of trying to crack the password, there didn't seem to be much so we started wpscan.
We found a few vulnerabilites but after attempting to use them, we seem to get some password hashes but cannot crack them.

Maybe we will try and exploit any misconfigurations of the server rather than premade exploits.

![[Pasted image 20241203174622.png]]

Here we have a vulnerability in the local files of the web server.
We also find a VHOST here:

![[Pasted image 20241203174735.png]]

Adding it to our /etc/hosts we receive this website:

![[Pasted image 20241203175115.png]]

Running wpscan for the original website and enumerating the users, we are able to find five usernames that should work:

- chooyu
- everest
- montblanc
- admin
- k2

We will first attempt to use the username as the password for each of the usernames:

![[Pasted image 20241203181638.png]]

We found the user k2 with the password k2 as a successful login.
Now we will check the website for any good information we can use to login as a shell.

![[Pasted image 20241203181942.png]]

Here we are able to find a password, we can attempt to login to wordpress using this password.
Now we have successfully logged in as k2 using the above password.

![[Pasted image 20241203182611.png]]

Now we have the wordpress version 6.4.3, looking online we find many vulnerabilities include a Remote Code Execution (RCE) vulnerability in CVE-2021-24145.

## Exploit

![[Pasted image 20241203183101.png]]

After running the exploit, we go to the link and we receive a web shell, however, we prefer to have a better shell so we will run a reverse shell payload on the shell to our local computer:

![[Pasted image 20241203183405.png]]

![[Pasted image 20241203183414.png]]

We will now upgrade our shell then continue with privilege escalation.

![[Pasted image 20241203183531.png]]

## Privilege Escalation

We can now upgrade our privilege by changing switching user to k2 by using the password we used to get into the roundcube mail server (k2).

![[Pasted image 20241203183825.png]]

In the home directory for k2 we find the sent mail for the user k2 to lhotse:

![[Pasted image 20241203184047.png]]

This is interesting but we will come back to that later if needed, we also see that we can access lhotse's home directory so we will move in there and see what is there:

![[Pasted image 20241203184226.png]]

Here we find a KeePass file and we will transfer it to our attacker machine by changing it to base64 and copying the data then decoding it on our attacker machine.
Now we will create a custom wordlist using cupp:

![[Pasted image 20241203184912.png]]

Now we will use john and the wordlist to try and crack the keepass:

![[Pasted image 20241203185019.png]]

And now we have found the password for keepass, we will now open the file using the password and look what we have found:

![[Pasted image 20241203185600.png]]

We are able to get the password for the kangchenjunga user, within their home directory we find the local.txt file and a non-empty .bash_history file: in the file we can see a failed attempt at changing user to root then the user wrote the root user's password in plain text.

![[Pasted image 20241203185813.png]]

Now we can move to become the root user:

![[Pasted image 20241203185853.png]]

Moving to the home directory for root, we are able to get the root.txt:

![[Pasted image 20241203190015.png]]
