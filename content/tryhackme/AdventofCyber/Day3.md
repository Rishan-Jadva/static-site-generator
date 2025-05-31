# (Day 3) - Advent of Cyber

Target IP - 10.10.153.110

## ELK Logs

Upon instruction from TryHackMe, we were told to narrow down our search from October 3rd 11:30am to October 3 12pm.
Here we see the logs:

![[Pasted image 20241204114458.png]]

Here we have many logs to look through, let's see if we can reduce the number of logs to sift through. Considering the proof of concept used by TryHackMe in the example, we see that the attacker uploaded a shell.php. We will search for this message using KLQ:

![[Pasted image 20241204114648.png]]

Nice, we have now narrowed our search down to 13 hits, a lot less to sift through.
Here we see that the location where our file is uploaded to is:

![[Pasted image 20241204115347.png]]

When we try to move to that location we cannot see anything so we will need to find out what Glitch did to get this shell uploaded:

![[Pasted image 20241204115812.png]]

Here we see the IP address that was mostly used for each of the shell.php requests, now we can also see that Glitch seems to have admin access as seen here:

![[Pasted image 20241204120018.png]]

So we need to find a way to login to the site as admin, we will go to the website and attempt to login using admin admin credentials:

![[Pasted image 20241204120224.png]]

Here we see that we need to enter an email, so we cannot just use admin as the email section of the login. However, we previously saw in the TryHackMe, some common usernames that may be used and one of which was in the format of an email:

![[Pasted image 20241204120403.png]]

So if we were to use the domain name frostypines.thm with the admin account we can try to login like below with password admin:

![[Pasted image 20241204120514.png]]

Success, we have access to the admin account:

![[Pasted image 20241204120549.png]]

Now moving to the /admin endpoint we see a dashboard:

![[Pasted image 20241204120701.png]]

By clicking on Add new Room we see that there is an area to add an image for the room which may result in a file inclusion vulnerability:

![[Pasted image 20241204121246.png]]

We will now upload a webshell.php that we found online:

![[Pasted image 20241204121413.png]]

We will now upload the shell.php file and move to this directory:

![[Pasted image 20241204121946.png]]

Just like in the logs.

Here we receive the webshell:

![[Pasted image 20241204122015.png]]

From here we can find the file to complete the room:

![[Pasted image 20241204122102.png]]
