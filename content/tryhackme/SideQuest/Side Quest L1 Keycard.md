# Advent of Cyber Side Quest - L1 Keycard

Upon opening the AoC sidequest room we are met with a zip file that we have to open using a password that we obtain from a L1 Keycard. In order to get this keycard we need to find it from the first 4 days of the regular rooms of the advent of cyber.

I had previously found the place where the keycard would be located when I first attempted the rooms. I had run an nmap scan on the first room of the advent of cyber and I had identified a port that was not used in that room at all. 

![[Pasted image 20241205183916.png]]

Here we have website running on port 8000, it looks like this:

![[Pasted image 20241205184011.png]]

Looking at this website, I remembered the name of the website (Bloatware-C2), this name was seen when completing the first day of the advent of cyber room for the first time, this was found previously on github, where we finished the room's final task:

![[Pasted image 20241205184748.png]]

After seeing this conversation, we the other user that was talking with Mayor Malware was Bloatware. So by heading to his profile, we can see that he has a C2 server repository:

![[Pasted image 20241205184934.png]]

Heading into the repository we see a flask C2 server that has some admin credentials and also interestingly a secret_key that is used to encrypt the session cookies and ensure's that the cookie provided in the browser is authentic and not spoofed. 

![[Pasted image 20241205185526.png]]

Attempting to login using the above credentials does not seem to work, so we may need to try and find a way to spoof the session cookie given that we have the secret_key for the app. As long as mayor malware has not changed this cookie, we should be able to login to this page.

We also identify in the code the cookie that we will need to make, it seems that once the user has logged in, a cookie for logged_in and username are set in this format:

```
session{
	'logged_in': 'true',
	'username': 'admin'
}
```

Now given this cookie, we need to encrypt it using the secret key and base64 encode it as well. However, this process may be a bit difficult so we will use a python script that I found online:

![[Pasted image 20241205190319.png]]

By downloading the 'flask_session_cookie_manager3.py' and checking the usage settings, we are able to obtain a cookie that we can place in the browser to hopefully successfully login:

![[Pasted image 20241205190714.png]]

Now let's place it as the browser cookie and attempt to move to another directory as seen in the flask application made by bloatware:

![[Pasted image 20241205190803.png]]

![[Pasted image 20241205190814.png]]

![[Pasted image 20241205190824.png]]

![[Pasted image 20241205190838.png]]

![[Pasted image 20241205190926.png]]

Now we will refresh the page and hopefully we should be able to move to a different endpoint:

![[Pasted image 20241205191343.png]]

Now we are able to see the dashboard, data and logout navbar elements which in the source code say:

![[Pasted image 20241205191420.png]]

This means that our cookie has worked however, by clicking any of the navbar links, it just returns us to the login page, let's open BurpSuite and try and capture the request to see if anything is going wrong:

![[Pasted image 20241205191950.png]]

We will send the request to Repeater to see if we can diagnose this issue:

![[Pasted image 20241205192056.png]]

Here we see that the cookie is not passed to the next page, now if we add the cookie and repeat the request again, we see this:

![[Pasted image 20241205192637.png]]

There are some new characters in the response, by rendering the response we see:

![[Pasted image 20241205192844.png]]

There doesn't seem to be much here that is very useful, let's maybe try the /data endpoint in BurpSuite:

![[Pasted image 20241205193205.png]]

Wow, we have found the Keycard but we cannot see what it says, let's check the source code to see if we can find the endpoint to load the image:

![[Pasted image 20241205193538.png]]

By heading to this endpoint in the browser, we see the keycard entirely:

![[Pasted image 20241205194025.png]]

Now we have the password to unlock our zip file.
