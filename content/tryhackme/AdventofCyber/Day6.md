# (Day 6) - Advent of Cyber

Target IP - 10.10.78.134

## Windows RDP

By starting up the Endpoint Detection and Response using the following command:

```
PS C:\Tools> .\JingleBells.ps1
```

This will monitor the event logs for any vulnerable malware that is running on the system, or accessing certain files that may be considered vulnerable or protected data. Now running the malware we receive this response in the EDR:

![[Pasted image 20241207010318.png]]

After running the malware we receive this notification:

![[Pasted image 20241207010420.png]]

Now we can try and use FLOSS where the malware may be encrypted or difficult for the regular EDR to detect. So now we receive a text file after running floss:

![[Pasted image 20241207010709.png]]

Now we will open the file and search for the thm flag:

![[Pasted image 20241207010804.png]]
