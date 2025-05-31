# (Day 15) - Advent of Cyber

## Active Directory

#### EventViewer

We will head to the security tab of EventViewer and there we see the following:

![[Pasted image 20241229193555.png]]

Now we can press `CTRL-F` and type in Glitch_Malware to search for the correct account logon, now we can see the date of logon here:

![[Pasted image 20241229193836.png]]

Additionally we can see the Event ID for the logon for Glitch_Malware.

#### Powershell History

By heading to the following location, we can use notepad to view the administrator powershell commands:
`%APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt`

There we see the following commands:

![[Pasted image 20241229194325.png]]

#### Powershell Logs

To find the password we will head to Application and Services Logs then Windows Powershell. Then we will search using `CTRL-F` for the string password. There we find the following:

![[Pasted image 20241229195247.png]]

#### Group Policy Object (GPO)

We will now open Powershell and run the command:

```
Get-GPO -All
```

There we see:

```
DisplayName      : Default Domain Policy                                                                                DomainName       : wareville.thm                                                                                        Owner            : WAREVILLE\Domain Admins                                                                              Id               : 31b2f340-016d-11d2-945f-00c04fb984f9                                                                 GpoStatus        : AllSettingsEnabled                                                                                   Description      :                                                                                                      CreationTime     : 10/14/2024 12:17:31 PM                                                                               ModificationTime : 10/14/2024 12:19:28 PM                                                                               UserVersion      : AD Version: 0, SysVol Version: 0                                                                     ComputerVersion  : AD Version: 3, SysVol Version: 3                                                                     WmiFilter        :                                                                                                                                                                                                                              DisplayName      : Default Domain Controllers Policy                                                                    DomainName       : wareville.thm                                                                                        Owner            : WAREVILLE\Domain Admins                                                                              Id               : 6ac1786c-016f-11d2-945f-00c04fb984f9                                                                 GpoStatus        : AllSettingsEnabled                                                                                   Description      :                                                                                                      CreationTime     : 10/14/2024 12:17:31 PM                                                                               ModificationTime : 10/14/2024 12:17:30 PM                                                                               UserVersion      : AD Version: 0, SysVol Version: 0                                                                     ComputerVersion  : AD Version: 1, SysVol Version: 1                                                                     WmiFilter        :                                                                                                                                                                                                                              DisplayName      : Malicious GPO - Glitch_Malware Persistence                                                           DomainName       : wareville.thm                                                                                        Owner            : WAREVILLE\Domain Admins                                                                              Id               : d634d7c1-db7a-4c7a-bf32-efca23d93a56                                                                 GpoStatus        : AllSettingsEnabled                                                                                   Description      : Malicious GPO to add backdoor user on all domain-joined machines                                     CreationTime     : 10/30/2024 9:01:36 AM                                                                                ModificationTime : 10/30/2024 9:01:36 AM                                                                                UserVersion      : AD Version: 0, SysVol Version: 0                                                                     ComputerVersion  : AD Version: 0, SysVol Version: 0                                                                     WmiFilter        :                                  
```

Here we identify a Malicious GPO - Glitch_Malware Persistence.
