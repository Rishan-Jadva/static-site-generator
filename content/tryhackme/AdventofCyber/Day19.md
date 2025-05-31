# (Day 19) - Advent of Cyber

## Game Hacking

Opening the game we see a penguin, interacting with him we see that we need some sort of OTP (One Time Password) as seen here:

![[Pasted image 20241230035851.png]]

So to understand what is going on, we will use frida with the following command:

```
frida-trace ./TryUnlockMe -i 'libaocgame.so!*'
```

There is opens the game, then when we interact with the OTPenguin we see a `_Z7set_otpi()` function here:

```
Instrumenting...                                                        
_Z17validate_purchaseiii: Loaded handler at "/home/ubuntu/Desktop/TryUnlockMe/__handlers__/libaocgame.so/_Z17validate_purchaseiii.js"
_Z7set_otpi: Loaded handler at "/home/ubuntu/Desktop/TryUnlockMe/__handlers__/libaocgame.so/_Z7set_otpi.js"
_Z14create_keycardPKc: Auto-generated handler at "/home/ubuntu/Desktop/TryUnlockMe/__handlers__/libaocgame.so/_Z14create_keycardPKc.js"
_Z16check_biometricsPKc: Loaded handler at "/home/ubuntu/Desktop/TryUnlockMe/__handlers__/libaocgame.so/_Z16check_biometricsPKc.js"
Started tracing 4 functions. Web UI available at http://localhost:1337/ 
           /* TID 0x7af */
 14544 ms  _Z7set_otpi()

```

So now frida would have opened a `__handlers__`  folder which we can open the `libaocgame.so` folder within it. Using the following commands:

```
cd /home/ubuntu/Desktop/TryUnlockMe/__handlers__/libaocgame.so/

code .
```

Opening the `_Z7set_otpi.js` file we see the following code:

```
defineHandler({
  onEnter(log, args, state) {
    log('_Z7set_otpi()');
  },

  onLeave(log, retval, state) {
  }
});
```

We will now modify the file so that we log out the OTP that is stored in `args[0]`:

```
defineHandler({
  onEnter(log, args, state) {
    log('_Z7set_otpi()');
    log('Parameter:' + args[0].toInt32());
  },

  onLeave(log, retval, state) {
  }
});
```

Now we will rerun the previous frida command:

```
frida-trace ./TryUnlockMe -i 'libaocgame.so!*'
```

Then after interacting with the penguin we see the OTP:

```
Started tracing 4 functions. Web UI available at http://localhost:1337/ 
           /* TID 0x976 */
  7409 ms  _Z7set_otpi()
  7409 ms  Parameter:311650
```

Then after inputting the OTP we receive the following flag:

![[Pasted image 20241230042352.png]]

Now we move to the next stage where the penguin has a store however, the flag is set at 1,000,000 coins. So we cannot attempt to purchase it because it is much too expensive. 

When we check the function that is run when we attempt to purchase the flag we see the following function attempting to run:

```
83081 ms  _Z17validate_purchaseiii()
```

Heading to that function within the code we see the following:

```
defineHandler({
  onEnter(log, args, state) {
    log('_Z17validate_purchaseiii()');
  },

  onLeave(log, retval, state) {
  }
});
```

So now what we need to do is log out each of the integer parameters to make it look like the following:

```
defineHandler({
  onEnter(log, args, state) {
    log('_Z17validate_purchaseiii()');
    log('Param1: ' + args[0]);
    log('Param2: ' + args[1]);
    log('Param3: ' + args[2]);
  },

  onLeave(log, retval, state) {
  }
});
```

Now when running frida we see the following output:

```
 36128 ms  Param1: 0x3
 36128 ms  Param2: 0xf4240
 36128 ms  Param3: 0x1
```

So now we can assume that the first parameter is the itemID, the second parameter is the price of the item and the third parameter is the player's balance. Considering this we can manipulate the second parameter to be 0 so that we can purchase the flag, to do this we will modify the code to the following:

```
defineHandler({
  onEnter(log, args, state) {
    log('_Z17validate_purchaseiii()');
    log('Param1: ' + args[0]);
    log('Param2: ' + args[1]);
    log('Param3: ' + args[2]);
    args[1] = ptr(0)
  },

  onLeave(log, retval, state) {
  }
});
```

Running the following we are able to obtain the second flag:

![[Pasted image 20241230055603.png]]

Now preceding to the final stage we see another penguin that check's the biometric data of the player. We can see the function that it calls is:

```
 88130 ms  _Z16check_biometricsPKc()
```

Looking at the javascript code that is associated to that function we see the following:

```
defineHandler({
  onEnter(log, args, state) {
    log('_Z16check_biometricsPKc()');
  },

  onLeave(log, retval, state) {
  }
});
```

Upon seeing the name of the function we see that the type of the data that is being sent is a string which means we will have to log the information a little differently:

```
defineHandler({
  onEnter(log, args, state) {
    log('_Z16check_biometricsPKc()');
    log('Parameter: ' + Memory.readCString(args[0]));
  },

  onLeave(log, retval, state) {
  }
});
```

There we see the following which doesn't seem helpful to our situation:

```
43339 ms  _Z16check_biometricsPKc()
43339 ms  Paramter: TKEYoHuUKLF8PqFA1oxnMcNHIwNWCpLg7aEtr6O9RdHpTXxULtFhVbxoXKIh7eLE
```

So now instead we will log the return value to see if would be helpful, we can do this by modifying the javascript file like so:

```
defineHandler({
  onEnter(log, args, state) {
    log('_Z16check_biometricsPKc()');
    log('Parameter: ' + Memory.readCString(args[0]));
  },

  onLeave(log, retval, state) {
	log('Retval: ' + retval);
  }
});
```

Upon running the game again we see the following output:

```
49551 ms  Retval: 0x0
```

This may indicate that a false output is provided back to game considering that the name of the function is `check_biometrics`, it makes sense that it would return a boolean value, so instead of returning a 0 we should return a 1 for true. We can modify the code as follows to change the return value to a 1:

```
defineHandler({
  onEnter(log, args, state) {
    log('_Z16check_biometricsPKc()');
    log('Parameter: ' + Memory.readCString(args[0]));
  },

  onLeave(log, retval, state) {
	log('Retval: ' + retval);
	retval.replace(ptr(1));
  }
});
```

Now running the game another time we are successfully able to obtain the final flag:

![[Pasted image 20241230061414.png]]
