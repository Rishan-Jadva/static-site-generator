# HTB - Mirai

Target IP - 10.10.10.48

## Enumeration

#### Nmap

The first step in enumerating a target system is to run an nmap scan using the following command:

```
nmap 10.10.10.48 -p- -sC -sV -vv --min-rate 10000
```

From that command, we receive the following response:

![[Pasted image 20250103194027.png]]

Above we see some ports that are interesting, these are:

- SSH (Port 22)
- HTTP (Port 80, 32400)

#### Gobuster

Due to the fact that we don't have any credentials, we cannot currently access SSH. So now we will continue enumerating both websites using the following commands:

```
gobuster dir -u http://10.10.10.48 -w /usr/share/wordlists/dirb/common.txt 
gobuster dir -u http://10.10.10.48:32400 -w /usr/share/wordlists/dirb/common.txt 
```

From these commands, we receive the following:

![[Pasted image 20250103194725.png]]

![[Pasted image 20250103194747.png]]

Considering the fact that the second command doesn't work and that we find an interesting directory in the first output, we will ignore the second website for now.

## Website

Heading to the following link `http://10.10.10.48/admin` we see the following page.

![[Pasted image 20250103195320.png]]

Searching online we see that this is a server that is run on a raspberry pi. 

## Exploitation

#### Default Credentials

Knowing the server software that is being used, we can search online to try and find default credentials for this software. From this search we obtain the following values:

- `Username: pi`
- `Password: raspberry`

Using these values we are able to login to the target system via SSH.

![[Pasted image 20250103195815.png]]

After obtaining a shell as pi, we will now enumerate the system, going to the home directory then the desktop of the user we see the user.txt:

![[Pasted image 20250103200202.png]]

`ff837707441b257a20e32199d7c8838d`

## Privilege Escalation

By running the command `sudo -l` we are able to see what commands the user `pi` is able to run, from the output of the command we can see that the user has full access on this system, so just to confirm that we have full access we will run the command: `sudo su` so that we can become the official root user and read the root.txt that is usually present in the /root directory.

![[Pasted image 20250103200312.png]]

Unfortunately the root.txt is not present in its original form, now we are instructed to check a USB stick as a backup. To do so we will need to run the following command `df -h` so that we can see where these files are mounted:

![[Pasted image 20250103201027.png]]

Here we see the usbstick is in the media directory, heading to the directory then going into the stick we don't see the root.txt file but we do see a damnit.txt file:

![[Pasted image 20250103200641.png]]

So now we understand that the root.txt has been deleted off the USB, however, if the data has not been overwritten or reformatted then the data can still be there just not visible.
To access this information, we will have to go to the raw device itself and not the pretty filesystem mount that has been made for us. Previously we ran the command `df -h` and from that we say that the usbstick was in the media directory, but now rather than looking at the mount we want to know where the filesystem is so that we can read data directly off of it. To do so we will read the strings of the following directory:

```
strings /dev/sdb
```

From this command we see the following data recovered:

```
>r &
/media/usbstick
lost+found
root.txt
damnit.txt
>r &
>r &
/media/usbstick
lost+found
root.txt
damnit.txt
>r &
/media/usbstick
2]8^
lost+found
root.txt
damnit.txt
>r &
"3d3e483143ff12ec505d026fa13e020b"
Damnit! Sorry man I accidentally deleted your files off the USB stick.
Do you know if there is any way to get them back?
-James
```

Here we see an interesting set of characters which turns out to be our flag.