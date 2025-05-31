# (Day 12) - Advent of Cyber

Target IP - 10.10.244.217

## Web Timings and Race Conditions

## Website

![[Pasted image 20241227170837.png]]

Here we are greeted with a login page and we are instructed to login as glitch using the following account number and password:

```
Account_Number: 101
Password: glitch
```

Logging in, we see that we are able to transfer the funds as instructed but before we do we will capture a request in Burpsuite.

![[Pasted image 20241227171510.png]]

#### Burpsuite

We will capture a POST request for transferring funds from one account to another and send it to repeater.

![[Pasted image 20241227171900.png]]

We will now duplicate these requests and add them to a tab group, then send the requests in parallel, now we can reload the page and see a negative balance in the glitch's account:

![[Pasted image 20241227172339.png]]

There we receive the flag.