# (Day 7) - Advent of Cyber

## CloudWatch Log Analysis

Upon opening the vm we are able to head to the /wareville_logs directory and there we see the following:

![[Pasted image 20241217183625.png]]

We can use jq to analyse and filter the appropriate information out from the .json file.
By using the following command:

```
jq -r '["Event_Time", "Event_Name", "User_Name", "Bucket_Name", "Key", "Source_IP"], (.Records[] | select(.eventSource == "s3.amazonaws.com" and .requestParameters.bucketName == "wareville-care4wares") | [.eventTime, .eventName, .userIdentity.userName // "N/A", .requestParameters.bucketName // "N/A", .requestParameters.key // "N/A", .sourceIPAddress // "N/A"]) | @tsv' cloudtrail_log.json | column -t
```

We are able to receive the following results in a easy to read format:

```
Event_Time            Event_Name        User_Name  Bucket_Name           Key                                         Source_IP
2024-11-28T15:22:23Z  ListObjects       glitch     wareville-care4wares  N/A                                         53.94.201.69
2024-11-28T15:22:25Z  ListObjects       glitch     wareville-care4wares  N/A                                         53.94.201.69
2024-11-28T15:22:39Z  PutObject         glitch     wareville-care4wares  bank-details/wareville-bank-account-qr.png  53.94.201.69
2024-11-28T15:22:39Z  PreflightRequest  N/A        wareville-care4wares  bank-details/wareville-bank-account-qr.png  53.94.201.69
2024-11-28T15:22:44Z  ListObjects       glitch     wareville-care4wares  N/A                                         53.94.201.69
```

There we find that a user glitch caused an event PutObject which seems to be the time that which the fake payment image was uploaded.
Additionally, we also see the IP address that this user used to complete the actions.

Now given the user glitch, we can search up the events related to this user using this command:

```
jq -r '["Event_Time", "Event_type", "Event_Name", "User_Name", "Source_IP", "User_Agent"], (.Records[] | select(.userIdentity.userName == "glitch") | [.eventTime, .eventType, .eventName, .userIdentity.userName // "N/A", .sourceIPAddress // "N/A", .userAgent // "N/A"]) | @tsv' wareville_logs/cloudtrail_log.json | column -t -s $'\t'
```

There we are able to see the events related to the username:

```
Event_Time            Event_type        Event_Name                           User_Name  Source_IP     User_Agent
2024-11-28T15:22:12Z  AwsApiCall        HeadBucket                           glitch     53.94.201.69  [S3Console/0.4, aws-internal/3 aws-sdk-java/1.12.750 Linux/5.10.226-192.879.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.412-b09 java/1.8.0_412 vendor/Oracle_Corporation cfg/retry-mode/standard]
2024-11-28T15:22:23Z  AwsApiCall        ListObjects                          glitch     53.94.201.69  [S3Console/0.4, aws-internal/3 aws-sdk-java/1.12.750 Linux/5.10.226-192.879.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.412-b09 java/1.8.0_412 vendor/Oracle_Corporation cfg/retry-mode/standard]
2024-11-28T15:22:25Z  AwsApiCall        ListObjects                          glitch     53.94.201.69  [S3Console/0.4, aws-internal/3 aws-sdk-java/1.12.750 Linux/5.10.226-192.879.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.412-b09 java/1.8.0_412 vendor/Oracle_Corporation cfg/retry-mode/standard]
2024-11-28T15:22:39Z  AwsApiCall        PutObject                            glitch     53.94.201.69  [Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36]
2024-11-28T15:22:44Z  AwsApiCall        ListObjects                          glitch     53.94.201.69  [S3Console/0.4, aws-internal/3 aws-sdk-java/1.12.750 Linux/5.10.226-193.880.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.412-b09 java/1.8.0_412 vendor/Oracle_Corporation cfg/retry-mode/standard]
2024-11-28T15:21:54Z  AwsConsoleSignIn  ConsoleLogin                         glitch     53.94.201.69  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
2024-11-28T15:21:57Z  AwsApiCall        GetCostAndUsage                      glitch     53.94.201.69  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
2024-11-28T15:21:57Z  AwsApiCall        ListEnrollmentStatuses               glitch     53.94.201.69  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
2024-11-28T15:21:57Z  AwsApiCall        DescribeEventAggregates              glitch     53.94.201.69  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
2024-11-28T15:22:12Z  AwsApiCall        ListBuckets                          glitch     53.94.201.69  [S3Console/0.4, aws-internal/3 aws-sdk-java/1.12.750 Linux/5.10.226-193.880.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.412-b09 java/1.8.0_412 vendor/Oracle_Corporation cfg/retry-mode/standard]
2024-11-28T15:22:14Z  AwsApiCall        GetStorageLensConfiguration          glitch     AWS Internal  AWS Internal
2024-11-28T15:22:14Z  AwsApiCall        GetStorageLensDashboardDataInternal  glitch     AWS Internal  AWS Internal
2024-11-28T15:22:13Z  AwsApiCall        GetStorageLensDashboardDataInternal  glitch     AWS Internal  AWS Internal
2024-11-28T15:21:57Z  AwsApiCall        DescribeEventAggregates              glitch     53.94.201.69  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
2024-11-28T15:21:57Z  AwsApiCall        GetCostAndUsage                      glitch     53.94.201.69  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
```

Upon looking at the results we see an event name called `ConsoleLogin` however, we need to find what AWS service was the source of this event, to do this we will use the following command:

```
jq -r '["Event_Time", "Event_Source", "Event_Name", "User_Name", "Source_IP"], (.Records[] | select(.userIdentity.userName == "glitch") | [.eventTime, .eventSource, .eventName, .userIdentity.userName // "N/A", .sourceIPAddress // "N/A"]) | @tsv' wareville_logs/cloudtrail_log.json | column -t -s $'\t'
```

There we receive:

```
Event_Time            Event_Source                         Event_Name                           User_Name  Source_IP
2024-11-28T15:22:12Z  s3.amazonaws.com                     HeadBucket                           glitch     53.94.201.69
2024-11-28T15:22:23Z  s3.amazonaws.com                     ListObjects                          glitch     53.94.201.69
2024-11-28T15:22:25Z  s3.amazonaws.com                     ListObjects                          glitch     53.94.201.69
2024-11-28T15:22:39Z  s3.amazonaws.com                     PutObject                            glitch     53.94.201.69
2024-11-28T15:22:44Z  s3.amazonaws.com                     ListObjects                          glitch     53.94.201.69
2024-11-28T15:21:54Z  signin.amazonaws.com                 ConsoleLogin                         glitch     53.94.201.69
2024-11-28T15:21:57Z  ce.amazonaws.com                     GetCostAndUsage                      glitch     53.94.201.69
2024-11-28T15:21:57Z  cost-optimization-hub.amazonaws.com  ListEnrollmentStatuses               glitch     53.94.201.69
2024-11-28T15:21:57Z  health.amazonaws.com                 DescribeEventAggregates              glitch     53.94.201.69
2024-11-28T15:22:12Z  s3.amazonaws.com                     ListBuckets                          glitch     53.94.201.69
2024-11-28T15:22:14Z  s3.amazonaws.com                     GetStorageLensConfiguration          glitch     AWS Internal
2024-11-28T15:22:14Z  s3.amazonaws.com                     GetStorageLensDashboardDataInternal  glitch     AWS Internal
2024-11-28T15:22:13Z  s3.amazonaws.com                     GetStorageLensDashboardDataInternal  glitch     AWS Internal
2024-11-28T15:21:57Z  health.amazonaws.com                 DescribeEventAggregates              glitch     53.94.201.69
2024-11-28T15:21:57Z  ce.amazonaws.com                     GetCostAndUsage                      glitch     53.94.201.69
```

Now we are able to see the `Event_Source` for the `ConsoleLogin`.
There we are also able to get the time of the login to the glitch user.

Now we are asked what was the name of the user that mcskidy made, in order to do this we will use this command:

```
jq -r '["Event_Time", "Event_Source", "Event_Name", "User_Name", "Source_IP"], (.Records[] | select(.eventSource == "iam.amazonaws.com") | [.eventTime, .eventSource, .eventName, .userIdentity.userName // "N/A", .sourceIPAddress // "N/A"]) | @tsv' wareville_logs/cloudtrail_log.json | column -t -s $'\t'
```

We receive this from the command:

```
Event_Time            Event_Source       Event_Name          User_Name  Source_IP
2024-11-28T15:21:26Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:29Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:25Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com  GetPolicy           mcskidy    53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com  GetPolicy           mcskidy    53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com  GetPolicy           mcskidy    53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com  GetPolicy           mcskidy    53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:36Z  iam.amazonaws.com  CreateLoginProfile  mcskidy    53.94.201.69
2024-11-28T15:21:36Z  iam.amazonaws.com  AttachUserPolicy    mcskidy    53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:44Z  iam.amazonaws.com  ListUsers           mcskidy    53.94.201.69
2024-11-28T15:21:35Z  iam.amazonaws.com  CreateUser          mcskidy    53.94.201.69
```

In this output we see that the user mcskidy created a new user, to find information about this new user we will use the command:

```
jq '.Records[] | select(.eventSource == "iam.amazonaws.com" and .eventName == "CreateUser")' wareville_logs/cloudtrail_log.json
```

Receiving this output:
```
{
  "eventVersion": "1.10",
  "userIdentity": {
    "type": "IAMUser",
    "principalId": "AIDAXRMKYT5O6Z6AZBXU6",
    "arn": "arn:aws:iam::518371450717:user/mcskidy",
    "accountId": "518371450717",
    "accessKeyId": "ASIAXRMKYT5OVOMUJU3P",
    "userName": "mcskidy",
    "sessionContext": {
      "attributes": {
        "creationDate": "2024-11-28T15:20:54Z",
        "mfaAuthenticated": "false"
      }
    }
  },
  "eventTime": "2024-11-28T15:21:35Z",
  "eventSource": "iam.amazonaws.com",
  "eventName": "CreateUser",
  "awsRegion": "ap-southeast-1",
  "sourceIPAddress": "53.94.201.69",
  "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
  "requestParameters": {
    "userName": "glitch"
  },
  "responseElements": {
    "user": {
      "path": "/",
      "userName": "glitch",
      "userId": "AIDAXRMKYT5O7SKYSEJBQ",
      "arn": "arn:aws:iam::518371450717:user/glitch",
      "createDate": "Oct 22, 2024 3:21:35 PM"
    }
  },
  "requestID": "415e0a96-f1b6-429a-9cac-1c921c0b85f5",
  "eventID": "64dd59fc-c1b1-4f2d-b15c-b005911f1de4",
  "readOnly": false,
  "eventType": "AwsApiCall",
  "managementEvent": true,
  "recipientAccountId": "518371450717",
  "eventCategory": "Management",
  "tlsDetails": {
    "tlsVersion": "TLSv1.3",
    "cipherSuite": "TLS_AES_128_GCM_SHA256",
    "clientProvidedHostHeader": "iam.amazonaws.com"
  },
  "sessionCredentialFromConsole": "true"
}
```

Within this output we are able to obtain that the user mcskidy created the user under the name glitch.
In order to understand the access that was given to the user glitch, we need to identify and filter for the AttachUserPolicy event using the following command:

```
jq '.Records[] | select(.eventSource == "iam.amazonaws.com" and .eventName == "AttachUserPolicy")' cloudtrail_log.json
```

There we receive this json:

```
{
  "eventVersion": "1.10",
  "userIdentity": {
    "type": "IAMUser",
    "principalId": "AIDAXRMKYT5O6Z6AZBXU6",
    "arn": "arn:aws:iam::518371450717:user/mcskidy",
    "accountId": "518371450717",
    "accessKeyId": "ASIAXRMKYT5OVOMUJU3P",
    "userName": "mcskidy",
    "sessionContext": {
      "attributes": {
        "creationDate": "2024-11-28T15:20:54Z",
        "mfaAuthenticated": "false"
      }
    }
  },
  "eventTime": "2024-11-28T15:21:36Z",
  "eventSource": "iam.amazonaws.com",
  "eventName": "AttachUserPolicy",
  "awsRegion": "ap-southeast-1",
  "sourceIPAddress": "53.94.201.69",
  "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
  "requestParameters": {
    "userName": "glitch",
    "policyArn": "arn:aws:iam::aws:policy/AdministratorAccess"
  },
  "responseElements": null,
  "requestID": "975d9d18-27d5-48a8-a882-a8b58b3a7173",
  "eventID": "08799cc5-535f-4d58-8373-d0b2cbb73a52",
  "readOnly": false,
  "eventType": "AwsApiCall",
  "managementEvent": true,
  "recipientAccountId": "518371450717",
  "eventCategory": "Management",
  "tlsDetails": {
    "tlsVersion": "TLSv1.3",
    "cipherSuite": "TLS_AES_128_GCM_SHA256",
    "clientProvidedHostHeader": "iam.amazonaws.com"
  },
  "sessionCredentialFromConsole": "true"
}
```

Within this output we see that the user mcskidy attached the user glitch with administrator access.
Next we need to find out the IP Address that mcskidy uses to login to the system. We can do this by running this command:

```
jq -r '["Event_Time", "Event_Source", "Event_Name", "User_Name", "Source_IP"], (.Records[] | select(.sourceIPAddress == "53.94.201.69") | [.eventTime, .eventSource, .eventName, .userIdentity.userName // "N/A", .sourceIPAddress // "N/A"]) | @tsv' cloudtrail_log.json | column -t -s $'\t'
```

This is what we receive:

```
Event_Time            Event_Source                         Event_Name               User_Name      Source_IP
2024-11-28T15:20:38Z  s3.amazonaws.com                     HeadBucket               mayor_malware  53.94.201.69
2024-11-28T15:22:12Z  s3.amazonaws.com                     HeadBucket               glitch         53.94.201.69
2024-11-28T15:22:23Z  s3.amazonaws.com                     ListObjects              glitch         53.94.201.69
2024-11-28T15:22:25Z  s3.amazonaws.com                     ListObjects              glitch         53.94.201.69
2024-11-28T15:22:39Z  s3.amazonaws.com                     PutObject                glitch         53.94.201.69
2024-11-28T15:22:39Z  s3.amazonaws.com                     PreflightRequest         N/A            53.94.201.69
2024-11-28T15:22:44Z  s3.amazonaws.com                     ListObjects              glitch         53.94.201.69
2024-11-28T15:18:37Z  signin.amazonaws.com                 ConsoleLogin             mayor_malware  53.94.201.69
2024-11-28T15:20:54Z  signin.amazonaws.com                 ConsoleLogin             mcskidy        53.94.201.69
2024-11-28T15:21:54Z  signin.amazonaws.com                 ConsoleLogin             glitch         53.94.201.69
2024-11-28T15:21:26Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:29Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:25Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com                    GetPolicy                mcskidy        53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com                    GetPolicy                mcskidy        53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com                    GetPolicy                mcskidy        53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com                    GetPolicy                mcskidy        53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:36Z  iam.amazonaws.com                    CreateLoginProfile       mcskidy        53.94.201.69
2024-11-28T15:21:36Z  iam.amazonaws.com                    AttachUserPolicy         mcskidy        53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:44Z  iam.amazonaws.com                    ListUsers                mcskidy        53.94.201.69
2024-11-28T15:21:35Z  iam.amazonaws.com                    CreateUser               mcskidy        53.94.201.69
2024-11-28T15:21:45Z  organizations.amazonaws.com          DescribeOrganization     mcskidy        53.94.201.69
2024-11-28T15:21:57Z  ce.amazonaws.com                     GetCostAndUsage          glitch         53.94.201.69
2024-11-28T15:21:57Z  cost-optimization-hub.amazonaws.com  ListEnrollmentStatuses   glitch         53.94.201.69
2024-11-28T15:21:57Z  health.amazonaws.com                 DescribeEventAggregates  glitch         53.94.201.69
2024-11-28T15:22:12Z  s3.amazonaws.com                     ListBuckets              glitch         53.94.201.69
2024-11-28T15:21:57Z  health.amazonaws.com                 DescribeEventAggregates  glitch         53.94.201.69
2024-11-28T15:21:57Z  ce.amazonaws.com                     GetCostAndUsage          glitch         53.94.201.69
2024-11-22T11:08:03Z  signin.amazonaws.com                 ConsoleLogin             mayor_malware  53.94.201.69
2024-11-23T07:19:01Z  signin.amazonaws.com                 ConsoleLogin             mayor_malware  53.94.201.69
2024-11-24T02:28:17Z  signin.amazonaws.com                 ConsoleLogin             mayor_malware  53.94.201.69
2024-11-25T21:48:22Z  signin.amazonaws.com                 ConsoleLogin             mayor_malware  53.94.201.69
2024-11-26T22:55:51Z  signin.amazonaws.com                 ConsoleLogin             mayor_malware  53.94.201.69
```

Here we see that mcskidy and glitch both use the same IP Address. But to check if mcskidy always uses the same IP address we can run the following command:

```
jq -r '["Event_Time", "Event_Source", "Event_Name", "User_Name", "User_Agent", "Source_IP"], (.Records[] | select(.userIdentity.userName == "mcskidy") | [.eventTime, .eventSource, .eventName, .userIdentity.userName // "N/A", .userAgent // "N/A", .sourceIPAddress // "N/A"]) | @tsv' cloudtrail_log.json | column -t -s $'\t'
```

Given this command we are able to find out mcskidy's real IP Address here:

```
Event_Time            Event_Source                 Event_Name            User_Name  User_Agent                                                                                                             Source_IP
2024-11-28T15:20:54Z  signin.amazonaws.com         ConsoleLogin          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:26Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:29Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:25Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com            GetPolicy             mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com            GetPolicy             mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com            GetPolicy             mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com            GetPolicy             mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:36Z  iam.amazonaws.com            CreateLoginProfile    mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:36Z  iam.amazonaws.com            AttachUserPolicy      mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com            ListPolicies          mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:44Z  iam.amazonaws.com            ListUsers             mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:35Z  iam.amazonaws.com            CreateUser            mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-28T15:21:45Z  organizations.amazonaws.com  DescribeOrganization  mcskidy    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36  53.94.201.69
2024-11-22T12:20:54Z  signin.amazonaws.com         ConsoleLogin          mcskidy    Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36        31.210.15.79
2024-11-23T07:15:54Z  signin.amazonaws.com         ConsoleLogin          mcskidy    Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36        31.210.15.79
2024-11-24T05:19:31Z  signin.amazonaws.com         ConsoleLogin          mcskidy    Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36        31.210.15.79
2024-11-25T01:11:32Z  signin.amazonaws.com         ConsoleLogin          mcskidy    Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36        31.210.15.79
2024-11-26T19:22:05Z  signin.amazonaws.com         ConsoleLogin          mcskidy    Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36        31.210.15.79
```

Now to find the bank account number for Mayor Malware, we can take a look in the `rds.log` using the following command:

```
grep 'Mayor Malware' rds.log
```

In the output of this command we receive many lines in relation to Mayor Malware's transaction history (trimmed):

```
# shortened
2024-11-28T15:23:02.605Z 2024-11-28T15:23:02.605700Z	  263 Query	INSERT INTO wareville_bank_transactions (account_number, account_owner, amount) VALUES ('2394 6912 7723 1294', 'Mayor Malware', 193.45)
2024-11-28T15:23:02.792Z 2024-11-28T15:23:02.792161Z	  263 Query	INSERT INTO wareville_bank_transactions (account_number, account_owner, amount) VALUES ('2394 6912 7723 1294', 'Mayor Malware', 998.13)
2024-11-28T15:23:02.976Z 2024-11-28T15:23:02.976943Z	  263 Query	INSERT INTO wareville_bank_transactions (account_number, account_owner, amount) VALUES ('2394 6912 7723 1294', 'Mayor Malware', 865.75)
2024-11-28T15:23:03.161Z 2024-11-28T15:23:03.161700Z	  263 Query	INSERT INTO wareville_bank_transactions (account_number, account_owner, amount) VALUES ('2394 6912 7723 1294', 'Mayor Malware', 409.54)
2024-11-28T15:23:03.346Z 2024-11-28T15:23:03.346516Z	  263 Query	INSERT INTO wareville_bank_transactions (account_number, account_owner, amount) VALUES ('2394 6912 7723 1294', 'Mayor Malware', 251.99)
```

There we are able to see the `account_number` that is used.