# (Day 13) - Advent of Cyber

## Websockets

#### Website

Below is the car tracking website, that is able to provide live tracking of our car. Additionally, we are able to send messages to a community message board and receive messages live.

![[Pasted image 20241227193319.png]]

#### Burpsuite

We will now open burpsuite to capture websocket requests so that we can attempt to see other user's cars and send messages as another user. To do this we will first intercept the traffic then click the track button to see the websocket request to track a user (my user, that will change to another users's ) car:

![[Pasted image 20241227193955.png]]

As recommended, we will change the userId to 8 to track Mayor Malware's car. We will forward the request then turn intercept off to see the message flag that is written by mayor malware:

![[Pasted image 20241227194229.png]]

Now we will send a message as Mayor malware by writing a message then intercepting the traffic using Burpsuite before clicking send and obtaining the second flag after turning off intercept:

![[Pasted image 20241227194409.png]]

Changing the above to 8, forwarding and turning off intercept, we then see the following flag:

![[Pasted image 20241227195410.png]]
