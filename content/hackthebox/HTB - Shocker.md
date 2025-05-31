# HTB - Shocker

## Enumeration

#### Open Ports

- Port 80 - HTTP
- Port 2222 - SSH

#### Nmap Scan

![[Pasted image 20241205195431.png]]

## Website

Upon opening the website we see a simple image that says "Don't Bug Me!" and nothing else:

![[Pasted image 20241205195601.png]]

We will now need to run a gobuster scan to search for some hidden directories, we will use the dirb (common.txt) to make it quick:

![[Pasted image 20241206151530.png]]

Here we see that we have some access to /cgi-bin/ directory, after searching online we find vulnerabilities related to the cgi-bin directory. Let's try and find if there are any scripts in the cgi-bin vulnerability using gobuster for that directory:

![[Pasted image 20241206152717.png]]

By going to that directory we get the user.sh script, however, it does not seem like it is very useful:

![[Pasted image 20241206152803.png]]

## Exploit 

But previously, while searching I found and exploit-db vulnerability called 'shellshock' and it seems like the current machine is vulnerable to the script. Searching online for shellshock I find that there is a Proof of Concept (PoC) for this. By using this script I am able to get a reverse shell to my computer:

![[Pasted image 20241206153048.png]]

![[Pasted image 20241206153103.png]]

Now we can move to /home/shelly directory and find the user.txt for this machine.

## Privilege Escalation

By running sudo -l as shelly, we find that we can run the /usr/bin/perl binary. 

![[Pasted image 20241206153408.png]]

By searching GTFOBins we are able to find the command we can use to exploit the system:

![[Pasted image 20241206153428.png]]

After running this command we see that we are root:

![[Pasted image 20241206153503.png]]

Then by heading to the /root directory we get the root.txt.