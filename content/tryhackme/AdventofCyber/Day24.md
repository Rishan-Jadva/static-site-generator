# (Day 24) - Advent of Cyber

## MQTT & Wireshark

After opening the light switch application. We will open the challenge.pcapng file in wireshark. Within the packet capture we see the following packets:

![[Pasted image 20241231203317.png]]

Looking at the publish message packets we see the topic that all of the messages are talking about:

![[Pasted image 20241231203348.png]]

Therefore in order to talk to the light application through the terminal, we will need to use that topic. So making sure the light application is open we should be able to run the following command:

```
mosquitto_pub -h localhost -t "d2FyZXZpbGxl/Y2hyaXN0bWFzbGlnaHRz" -m "on"
```

So that in the light control application we see the flag:

![[Pasted image 20241231203512.png]]
