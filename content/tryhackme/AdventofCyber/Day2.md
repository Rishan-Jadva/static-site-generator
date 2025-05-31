# (Day 2) - Advent of Cyber

Target IP - 10.10.69.217

## Soc Application

By logging into the application using the provided credentials we find we SOC platform that we can use to identify possible intrusions into our system.

![[Pasted image 20241203152113.png]]

Now we should find the area that shows us any potential security alerts:

![[Pasted image 20241203152527.png]]

Here we have a security analytics page but the dates are set to 15 minutes ago and not from when the supposed attack occured, we will now update the date to the date of the attack Dec 1:

![[Pasted image 20241203152649.png]]

Now we have a bunch of hits for issues, especially with all of the repeated logon attempts occurring with the same username:

![[Pasted image 20241203153239.png]]

We also see that there are 6791 login failed requests during the period.
Now we can find out the IP address of Glitch:

![[Pasted image 20241203161611.png]]

Now we see the command executed by Glitch which helped restore the sytem to normal:

![[Pasted image 20241203163050.png]]

![[Pasted image 20241203163135.png]]
