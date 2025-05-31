# HTB - Grandpa

Target IP - 10.10.10.14

## Enumeration

#### Open Ports

- Port 80 - HTTP

#### Nmap Scan

![[Pasted image 20241201203719.png]]

## Exploit

As given by Nmap, the version for Microsoft IIS is 6.0, looking up online, we can find a vulnerability for this version under CVE-2017-7269.
There is a metasploit module that we can use to exploit this CVE:

![[Pasted image 20241201204153.png]]

We now get a meterpreter session for this system:

![[Pasted image 20241201204348.png]]

## Privilege Escalation

Now we will background the meterpreter session and use a post exploit module to find possible privilege escalation paths:

![[Pasted image 20241201205117.png]]

We will now run each exploit seeing if any help escalate our privilege successfully, however before we do so we need to make sure that we migrate the meterpreter session to a more stable process, then run the exploits. Many of them work but we do not have a session as NT AUTHORITY\SYSTEM.

![[Pasted image 20241201210438.png]]

So we need to keep running more exploits until we find the correct one that gives the right privileged user.

Here we find out that the exploit below gives the correct user:

![[Pasted image 20241201210820.png]]

Now that we are NT AUTHORITY\SYSTEM we are able to access all the files.