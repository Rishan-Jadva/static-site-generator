# (Day 4) - Advent of Cyber

Target IP - 10.10.248.168

## RDP Windows Emulator

![[Pasted image 20241205152537.png]]

In order to find the command and scripting interpreter command we need to search online for this with the MITREATT&CK keyword, there we find:

![[Pasted image 20241205152646.png]]

Then we are instructed to find the Windows Command Shell sub-technique, which we are able to get by opening the sub-techniques drop down:

![[Pasted image 20241205153020.png]]

Now, if we remember we were told to conduct a ransomware attack simulation, so if we check details of this command and scripting interpreter we see:

![[Pasted image 20241205153536.png]]

![[Pasted image 20241205153554.png]]

![[Pasted image 20241205153606.png]]

![[Pasted image 20241205153631.png]]

By the time we saw the 4th Test we see that it directly talks about a ransomware attack. So we will use that to advance and find the file that will be used in the attack.

So now we need to find the file that will be run during the attack. Here we will be a bit cheeky and in the details for the command it shows the location of the file that would be run during the attack:

![[Pasted image 20241205154317.png]]

So if we move and open this file we will be able to see the flag:

![[Pasted image 20241205154424.png]]
