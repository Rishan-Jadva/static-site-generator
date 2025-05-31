# (Day 20) - Advent of Cyber

## Wireshark Packet Analysis

The first step in analysing the packets is to filter the packets that are related to Marta May Ware's ip address, we will do this by using the following filter:

![[Pasted image 20241231142447.png]]

We additionally filter using http because this can be used to identify plaintext communication between the attacker and the webserver. Given that we know about a Command & Control server we see the following packets:

![[Pasted image 20241231142723.png]]

So now our first task indicates that we want to know the first message sent to Mayor Malware's C2. To do this we will right click the first HTTP POST request /initial and click follow tcp stream. There we are able to see the messages sent to the C2 here:

![[Pasted image 20241231143131.png]]

The red message was the first message which is `I am in Mayor!`.
Looking at the first packet there we can see the ip address that indicates the C2 server here:

![[Pasted image 20241231143552.png]]

Since the IP address 10.10.229.217 was Marta May Ware's IP address we can deduce that the destination IP address is also the IP address of the C2 server.

Now to find out the commands that the attacker sends to the target machine we can right click the HTTP GET request in relation to the /command endpoint and follow the TCP stream and there we see that the command that was sent was:

![[Pasted image 20241231144208.png]]

The next step is to find out the name of the file that was exfiltrated. In order to do this we can once again see check the HTTP requests and there we see the endpoint /exfiltrate.

![[Pasted image 20241231145033.png]]

Now repeating the same step as before, following the tcp stream, we see the following filename:

![[Pasted image 20241231145139.png]]

Here we see:
- Filename: `credentials.txt`
- Encryption key: `1234567890abcdef1234567890abcdef`

Now in order to find the secret message we will check the beacons tcp stream. Here we see the first HTTP POST request related to the beacon.

![[Pasted image 20241231150029.png]]

Now we will head on to cyberchef and decrypt the following encrypted string using the above key using the possible aes ecd decrypt.

![[Pasted image 20241231151719.png]]
