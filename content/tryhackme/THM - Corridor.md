# THM - Corridor

## Website

![](Pasted%20image%2020250605001711.png)

Given the above room, after clicking each door, we can see a few different strings of characters in the URL:

![](Pasted%20image%2020250605001912.png)

Looking at the string of characters, it seems like it is a hash, heading to [https://crackstation.net/][https://crackstation.net/] we can input the hash and we see the following:

![](Pasted%20image%2020250605002742.png)

So here we see that we have an MD5 hash which results in `1`, seeing that this is in the URL, we can attempt to exploit an IDOR vulnerability where we instead place a `0` in the URL instead. 

But first we need to hash the `0`, to do so we will use the following website: [https://www.miraclesalad.com/webtools/md5.php][https://www.miraclesalad.com/webtools/md5.php] 

![](Pasted%20image%2020250605003100.png)

Now placing this hash in the URL, we can obtain the flag.

![](Pasted%20image%2020250605003140.png)

![](Pasted%20image%2020250605003151.png)

