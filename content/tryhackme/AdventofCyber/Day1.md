# (Day 1) - Advent of Cyber

Target IP - 10.10.157.70

## Enumeration

#### Open Ports

- Port 22 - SSH
- Port 80 - HTTP
- Port 8000 - HTTP

#### Nmap Scan

![[Pasted image 20241202032853.png]]

## Website

Here we see a website that looks like every other youtube to mp3/mp4 converter:

![[Pasted image 20241202032146.png]]

The next step is to see what would happen if we download an mp3 from the website, if there is anything malicious by the Glitch.

![[Pasted image 20241202032259.png]]

We downloaded the file and we received a zip after unzipping the file we see that we are given 2 files named song.mp3 and somg.mp3. Now that seems malicious to have a file that the user will run that has a similar name to the original file:

![[Pasted image 20241202032628.png]]

Running exiftool for each of the files we see some malicious information for the somg.mp3 file whereas the song.mp3 file looks fine:

![[Pasted image 20241202032922.png]]![[Pasted image 20241202032942.png]]

In the second file we see that it has a hidden script that tries to download and run a malicious powershell script from the web:
https://raw.githubusercontent.com/MM-WarevilleTHM/IS/refs/heads/main/IS.ps1

Going to the link we find the content of the powershell script that sends data to the command and control (C2) server at the link:
http://papash3ll.thm/data

Due to the fact that the previous link has a username MM-WarevilleTHM we will search for the profile under that user, there we find the user and the repositories that they own:

![[Pasted image 20241202033534.png]]

Here we see the previous repository that the malicious file was from but there is also another repository called M.M, now we will take a look:

![[Pasted image 20241202033802.png]]

There is only a README.md file but that gives information about who M.M is Mayor Malware.
We will now check the powershell script, within the script we find that Mayor Malware has a sort of signature:

![[Pasted image 20241202035256.png]]

By searching for the text "Created by the one and only M.M" on GitHub we find a repository with issues:
![[Pasted image 20241202035525.png]]

This is an example of OPSEC vulnerability where one thing can link to another and expose items that shouldn't be seen together.