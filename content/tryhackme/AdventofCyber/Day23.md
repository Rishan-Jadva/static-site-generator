# (Day 23) - Advent of Cyber

## Hash Cracking (Cryptography)

#### John the Ripper

Heading to the `/AOC2024` folder we see a few files that we need to crack.
Firstly, we will attempt to crack the hash1.txt file.

To determine what type of hash we should let john know about, we can use a python script called hash-id.py. However, before we use the file we need to copy the hash using the following command:

```
cat hash1.txt 
d956a72c83a895cb767bb5be8dba791395021dcece002b689cf3b5bf5aaa20ac
```

After copying the hash we will now make use of hash-id.py using this command:

```
python hash-id.py
/home/user/AOC2024/hash-id.py:13: SyntaxWarning: invalid escape sequence '\ '
  logo='''   #########################################################################
   #########################################################################
   #     __  __                     __           ______    _____           #
   #    /\ \/\ \                   /\ \         /\__  _\  /\  _ `\         #
   #    \ \ \_\ \     __      ____ \ \ \___     \/_/\ \/  \ \ \/\ \        #
   #     \ \  _  \  /'__`\   / ,__\ \ \  _ `\      \ \ \   \ \ \ \ \       #
   #      \ \ \ \ \/\ \_\ \_/\__, `\ \ \ \ \ \      \_\ \__ \ \ \_\ \      #
   #       \ \_\ \_\ \___ \_\/\____/  \ \_\ \_\     /\_____\ \ \____/      #
   #        \/_/\/_/\/__/\/_/\/___/    \/_/\/_/     \/_____/  \/___/  v1.2 #
   #                                                             By Zion3R #
   #                                                    www.Blackploit.com #
   #                                                   Root@Blackploit.com #
   #########################################################################
--------------------------------------------------
 HASH: d956a72c83a895cb767bb5be8dba791395021dcece002b689cf3b5bf5aaa20ac

Possible Hashs:
[+] SHA-256
[+] Haval-256

Least Possible Hashs:
[+] GOST R 34.11-94
[+] RipeMD-256
[+] SNEFRU-256
[+] SHA-256(HMAC)
[+] Haval-256(HMAC)
[+] RipeMD-256(HMAC)
[+] SNEFRU-256(HMAC)
[+] SHA-256(md5($pass))
[+] SHA-256(sha1($pass))
--------------------------------------------------
```

So now we have identified the type of hash, we can make use of john to crack the password using a specific wordlist:

```
john --format=raw-sha256 --wordlist=/usr/share/wordlists/rockyou.txt hash1.txt
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-SHA256 [SHA256 256/256 AVX2 8x])
Warning: poor OpenMP scalability for this hash type, consider --fork=2
Will run 2 OpenMP threads
Note: Passwords longer than 18 [worst case UTF-8] to 55 [ASCII] rejected
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status
0g 0:00:00:03 DONE (2024-12-31 09:00) 0g/s 4687Kp/s 4687Kc/s 4687KC/s (4510458faruk)..*7¡Vamos!
Session completed. 
```

However, we do not seem to have found the password, we may need to use some rules to attempt to detect small changes in hashes such as e.g. `Hello` with `H3llo`. 

```
john --format=raw-sha256 --rules=wordlist --wordlist=/usr/share/wordlists/rockyou.txt hash1.txt
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-SHA256 [SHA256 256/256 AVX2 8x])
Warning: poor OpenMP scalability for this hash type, consider --fork=2
Will run 2 OpenMP threads
Note: Passwords longer than 18 [worst case UTF-8] to 55 [ASCII] rejected
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status
Enabling duplicate candidate password suppressor
fluffycat12      (?)     
1g 0:00:00:16 DONE (2024-12-31 09:02) 0.05967g/s 2314Kp/s 2314Kc/s 2314KC/s markie182..cherrylee2
Use the "--show --format=Raw-SHA256" options to display all of the cracked passwords reliably
Session completed. 
```

We are able to find the password `fluffycat12`.

Now considering a pdf file that is password protected, we can also use john to crack the password, however, we need to make the pdf file password hash into a format that john can understand and is able to crack. So we will need to do the following:

```
pdf2john.pl private.pdf > pdf.hash
john --rules=single --wordlist=wordlist.txt pdf.hash
Using default input encoding: UTF-8
Loaded 1 password hash (PDF [MD5 SHA2 RC4/AES 32/64])
Cost 1 (revision) is 3 for all loaded hashes
Will run 2 OpenMP threads
Note: Passwords longer than 10 [worst case UTF-8] to 32 [ASCII] rejected
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status
Enabling duplicate candidate password suppressor
M4y0rM41w4r3     (private.pdf)     
1g 0:00:00:00 DONE (2024-12-31 09:06) 3.704g/s 4503p/s 4503c/s 4503C/s mayored..afluffy
Use the "--show --format=PDF" options to display all of the cracked passwords reliably
Session completed. 
```

Now we have obtained the password: `M4y0rM41w4r3`. We can not open this pdf file and we receive the following flag: `THM{do_not_GET_CAUGHT}`
