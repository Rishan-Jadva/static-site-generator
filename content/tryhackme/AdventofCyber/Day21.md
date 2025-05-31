# (Day 21) - Advent of Cyber

## Reverse Engineering

Upon opening the windows VM we will open the PEStudio software and open the file located at /demo/demo.exe. 
So that we see the following:

![[Pasted image 20241231164544.png]]

By clicking the indicators we are able to identify and learn that the file is compiled using the .NET framework with the C# language as seen here:

![[Pasted image 20241231165433.png]]

Now we have the basic information about the executable we will now use the ILSpy tool to decompile the binary with readable information.
That should look something like this:

![[Pasted image 20241231170149.png]]

Heading to the main function, we are able to understand what the code is attempting to do:

![[Pasted image 20241231170616.png]]

Here we see the code is attempting to download an image and place it on the desktop of the user. 
Now we are tasked to perform reverse engineering on the WarevilleApp.exe. 

#### WarevilleApp.exe

Opening the following executable in the ILSpy software, we see the following:

![[Pasted image 20241231171206.png]]

We will now head to the form1 section:

![[Pasted image 20241231172117.png]]

Looking at this section, we find functions, one of which is very interesting:

![[Pasted image 20241231172319.png]]

This function downloads another binary called explorer.exe. This binary comes from the following domain name `mayorc2.thm`.

Now what we will now is run the following WarevilleApp.exe binary to obtain the explorer.exe binary so that we can decompile that binary. 
After running the binary and opening the explorer.exe binary in ILSpy we find out some new information in the following two functions:

![[Pasted image 20241231173540.png]]

![[Pasted image 20241231173553.png]]

Within the following functions we are able to see the name of the zip file: `CollectedFiles.zip`. 
Additionally we see the second c2 server used by Mayor Malware: `http://anonymousc2.thm/upload`

