# THM - Biohazard

Target IP: 10.10.190.138

## Enumeration

### Open Ports

- Port 21 - FTP
- Port 22 - SSH
- Port 80 - HTTP

### Enumerating the Web Server

Upon accessing the website, we are given the base site

![[Pasted image 20241128164656.png]]

We then click the link and are given this site

![[Pasted image 20241128164754.png]]

In the source code we find:

![[Pasted image 20241128164824.png]]

Upon accessing this page we find:

![[Pasted image 20241128164914.png]]

By clicking the link we find an emblem:

![[Pasted image 20241128165102.png]]

After looking in the source code for the dining room we find a base64 encoded string:

![[Pasted image 20241128165243.png]]

After decoding the string we obtain:

![[Pasted image 20241128165337.png]]

By travelling to this page, this is what we get:

![[Pasted image 20241128165454.png]]

By clicking the link we receive the lockpick flag:

![[Pasted image 20241128165544.png]]

The page suggests that we visit the art Room, upon visiting the page we see:

![[Pasted image 20241128165657.png]]

We are given a link to click after clicking it we are given a map of the website:

![[Pasted image 20241128165748.png]]

We begin to go to each new room, by going to the barRoom we discover the fact we need to use a lockpick we obtained earlier.

![[Pasted image 20241128170309.png]]

Upon entering the lockpick we enter the bar room:

![[Pasted image 20241128170359.png]]

There is a link to read moonlight somata, clicking this link we go a page with a code:

![[Pasted image 20241128170653.png]]

This is a base32 string when converted we receive:

![[Pasted image 20241128170753.png]]

Upon entering this sheet in the bar room we enter this page:

![[Pasted image 20241128170905.png]]

There is a link, once clicked we receive the emblem:

![[Pasted image 20241128171042.png]]

We are instructed to place this in an emblem slot on a previous page, we discover that by placing this emblem in the dining room we receive a code:

![[Pasted image 20241128171236.png]]

I believe this is a vignere cipher but I do not know the key. I refresh the secret bar page and place the original emblem in the slot that the gold emblem used to be, there we receive a name:

![[Pasted image 20241128174113.png]]

I believe this is the vignere cipher's key upon entering it into the decoder we find this:

![[Pasted image 20241128174309.png]]

By going to the page (/diningRoom/the_great_shield_key.html) we find this:

![[Pasted image 20241128174553.png]]

We then go to two different rooms starting with the armor room where a shield symbol is embedded into the door:

![[Pasted image 20241128174714.png]]

Upon entering the shield_key we get:

![[Pasted image 20241128174751.png]]

Upon clicking the link we get:

![[Pasted image 20241128174845.png]]

This is one part of a multipart cipher. We will continue to the next room before decoding the crests. We will go to the attic:

![[Pasted image 20241128174949.png]]

Entering the shield_key we get:

![[Pasted image 20241128175025.png]]

Reading the note we get:

![[Pasted image 20241128175051.png]]

There seems to be two more crests we will go back to the rooms we missed on the map, we will first head to the DiningRoom2F, here we find:

![[Pasted image 20241128175533.png]]

Checking the source code we find some encrypted text:

![[Pasted image 20241128175630.png]]

This encrypted text is encoded using ROT13 by decrypting we receive:

![[Pasted image 20241128180450.png]]

Going it the link we receive:

![[Pasted image 20241128180530.png]]

We then go to the tiger status room:

![[Pasted image 20241128180623.png]]

Placing the gem into the tiger's eye we get:

![[Pasted image 20241128180700.png]]

Looking in the gallery Room we find:

![[Pasted image 20241128181404.png]]

Following the link, we find the final crest:

![[Pasted image 20241128181429.png]]

By decoding all of the crests we get:

![[Pasted image 20241128181615.png]]

![[Pasted image 20241128181631.png]]

![[Pasted image 20241128181649.png]]

![[Pasted image 20241128181703.png]]

By putting them together and decoding we get:

![[Pasted image 20241128181801.png]]

### Enumerating FTP

Upon entering the FTP given the above credentials we see these files:

![[Pasted image 20241128182205.png]]

Once we get all of the files from FTP we can analyse each one.
We will start with seeing what important.txt says:

![[Pasted image 20241128182310.png]]

There seems to be a /hidden_closet/ webpage but it also needs the helmet_key.

Now looking at the three keys we were given, there doesn't seem to be anything visually worth looking at but we will first check using steghide to see if there are any hidden files located within the image.
Upon doing this we saw only one of the files had a hidden file in which we extracted.

![[Pasted image 20241128184509.png]]

Now we will check exiftool to see if there is any important information given in the keys.
Given that we already found a key in key-001 we will skip that file.

![[Pasted image 20241128184650.png]]

We find a comment with some text which we will extract to a new file.
Now we will use binwalk to check if there is anything extra in addition to the image information.

![[Pasted image 20241128184820.png]]

We see there is a zip in this image so we will unzip it cat there should be some text information.

![[Pasted image 20241128184904.png]]

Adding all three keys together then decrypting using base64 we get:

![[Pasted image 20241128185453.png]]

After decrypting the helmet_key file with gpg we receive:

![[Pasted image 20241128185552.png]]

Now going back to the closet room we can now enter the helmet_key:

![[Pasted image 20241128185711.png]]

In the Study Room we have a link which gives us a file called doom.tar.gz. Before we extract the file we will first check what is in the closet room:

![[Pasted image 20241128185849.png]]

Here we have two links, once clicked we get:

![[Pasted image 20241128185929.png]]

And:

![[Pasted image 20241128185945.png]]

The above text looks like a vignere cipher, so we may need to look at the doom.tar.gz file first.

![[Pasted image 20241128190206.png]]

Now we have all of the ssh information we need but we also have the cipher to keep in mind. Now let's use ssh to connect to the server.

![[Pasted image 20241128190444.png]]

Now we will check the files and directories we can access:

![[Pasted image 20241128190633.png]]

There seems to be nothing there but we will list all of the files and directories using:

![[Pasted image 20241128190701.png]]

There is and interesting directory called .jailcell. Upon entering this we see some interesting information regarding chris.

![[Pasted image 20241128190953.png]]

Now we have another name 'albert'. Now what if we use this name as the key for the vignere cipher that we found previously. 

![[Pasted image 20241128191611.png]]

We now have the login for weasker, so lets ssh into weasker.

![[Pasted image 20241128191734.png]]

We have also found some interesting information. Now we with run sudo -l and we see that we can run any command with root. 

![[Pasted image 20241128192053.png]]

Now we will move into the root directory and find the root.txt.

![[Pasted image 20241128192227.png]]

