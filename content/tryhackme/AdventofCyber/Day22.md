# (Day 22) - Advent of Cyber

## Kubernetes DFIR

#### Initialisation

```
minikube start
```

To confirm the cluster is up and running we can run the following command and make sure that the running column is (1/1) and STATUS is running:

```
kubectl get pods -n wareville
```

![[Pasted image 20241231181141.png]]

#### Logs

In order to recover the logs we need to connect to the pod using the following command:

```
kubectl exec -n wareville naughty-or-nice -it -- /bin/bash
```

Now we will review the Apache2 access logs through the following command:

```
cat /var/log/apache2/access.log
```

We don't see much but in the last log we see a very interesting log:

```
172.17.0.1 - - [29/Oct/2024:12:32:48 +0000] "GET /shelly.php?cmd=whoami HTTP/1.1" 200 224 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
```

This log is suspicious however, we do not have any other logs so we will now run the following commands to check the backups of the logs:

```
exit
cd /home/ubuntu/dfir_artefacts/
cat pod_apache2_access.log
```

Within the logs we identify certain logs, such as:

```
127.0.0.1 - - [29/Oct/2024:12:38:45 +0000] "GET /shelly.php?cmd=whoami HTTP/1.1" 200 224 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
127.0.0.1 - - [29/Oct/2024:12:38:53 +0000] "GET /shelly.php?cmd=whoami HTTP/1.1" 200 224 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
127.0.0.1 - - [29/Oct/2024:12:38:59 +0000] "GET /shelly.php?cmd=ls HTTP/1.1" 200 386 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
127.0.0.1 - - [29/Oct/2024:12:39:16 +0000] "GET /shelly.php?cmd=cat+db.php HTTP/1.1" 200 463 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
127.0.0.1 - - [29/Oct/2024:12:39:38 +0000] "GET /shelly.php?cmd=whoami HTTP/1.1" 200 224 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
127.0.0.1 - - [29/Oct/2024:12:39:46 +0000] "GET /shelly.php?cmd=which+nc HTTP/1.1" 200 215 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
```

There we are able to identify that the attacker is interacting with the shelly.php file, the attack read the db.php file and the attacker was checking if the tool nc which is typically used for reverse connections.

We don't have much else here so now we will need to investigate the docker registry using the following command:

```
docker ps
```

From this command we see the following information:

```
CONTAINER ID   IMAGE                                 COMMAND                  CREATED        STATUS          PORTS                                                                                                                                  NAMES
77fddf1ff1b8   registry:2.7                          "/entrypoint.sh /etc…"   2 months ago   Up 42 minutes   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp                                                                                              registry_priv
cd9ee77b8aa5   gcr.io/k8s-minikube/kicbase:v0.0.42   "/usr/local/bin/entr…"   9 months ago   Up 26 minutes   127.0.0.1:32772->22/tcp, 127.0.0.1:32771->2376/tcp, 127.0.0.1:32770->5000/tcp, 127.0.0.1:32769->8443/tcp, 127.0.0.1:32768->32443/tcp   minikube
```

Now we will connect to the instance to check for any interesting logs:

```
docker exec registry_priv ls -al /var/log
```

From which we receive the following:

```
total 12
drwxr-xr-x    2 root     root          4096 Nov 12  2021 .
drwxr-xr-x    1 root     root          4096 Nov 12  2021 ..
```

Here we see nothing however, docker itself keeps logs, so lets look at them:

```
docker logs registry_priv
```

There is a lot of information here, it is hard to read, so now we will use the previously downloaded version by heading to the following folder:

```
cd /home/ubuntu/dfir_artefacts/
```

And we will be using the following file: `docker-registry-logs.log`
We will look through the IP addresses using the following command:

```
cat docker-registry-logs.log | grep "HEAD" | cut -d ' ' -f 1
```

We receive the following IPs:

```
172.17.0.1
10.10.130.253
```

Here we see the IP 172.17.0.1 which is a known IP however, the IP 10.10.130.253 is not known to us.
Now we can search for all the logs which include the IP address:

```
cat docker-registry-logs.log | grep "10.10.130.253"
```

There we see some interesting logs:

```
10.10.130.253 - - [29/Oct/2024:12:26:40 +0000] "GET /v2/wishlistweb/manifests/latest HTTP/1.1" 200 6366 "" "docker/19.03.12 go/go1.13.10 git-commit/48a66213fe kernel/4.15.0-213-generic os/linux arch/amd64 UpstreamClient(Docker-Client/19.03.12 \\(linux\\))"
```

In this log we identify that the attacker has successfully managed to read the manifest for wishlistweb. We also understand the the user-agent was the docker client which means the docker CLI was used to access the registry, the connection came from 10.10.130.253 and the client was authenticated.

Now we can search for any PATCH HTTP methods to identify anyone who may have pushed a new image:

```
cat docker-registry-logs.log | grep "10.10.130.253" | grep "PATCH"
```

From there we discover the following:

```
10.10.130.253 - - [29/Oct/2024:12:34:28 +0000] "PATCH /v2/wishlistweb/blobs/uploads/29667052-1161-4ef0-aa89-dc40a2ff1bcb?_state=AYqTsngRJQiO8AkQuMPShxj8LsmV_ePzL0IgISK-N7N7Ik5hbWUiOiJ3aXNobGlzdHdlYiIsIlVVSUQiOiIyOTY2NzA1Mi0xMTYxLTRlZjAtYWE4OS1kYzQwYTJmZjFiY2IiLCJPZmZzZXQiOjAsIlN0YXJ0ZWRBdCI6IjIwMjQtMTAtMjlUMTI6MzQ6MjguNzA0Njc2NTM5WiJ9 HTTP/1.1" 202 0 "" "docker/19.03.12 go/go1.13.10 git-commit/48a66213fe kernel/4.15.0-213-generic os/linux arch/amd64 UpstreamClient(Docker-Client/19.03.12 \\(linux\\))"
10.10.130.253 - - [29/Oct/2024:12:34:31 +0000] "PATCH /v2/wishlistweb/blobs/uploads/7d53a7ab-7489-4580-9d60-057ded8d5b15?_state=qgIkGiYWdoRmfiuY42h1hpHXQM89dTDL3Ag7YsIUQA17Ik5hbWUiOiJ3aXNobGlzdHdlYiIsIlVVSUQiOiI3ZDUzYTdhYi03NDg5LTQ1ODAtOWQ2MC0wNTdkZWQ4ZDViMTUiLCJPZmZzZXQiOjAsIlN0YXJ0ZWRBdCI6IjIwMjQtMTAtMjlUMTI6MzQ6MzEuODEwNzI0NTQ1WiJ9 HTTP/1.1" 202 0 "" "docker/19.03.12 go/go1.13.10 git-commit/48a66213fe kernel/4.15.0-213-generic os/linux arch/amd64 UpstreamClient(Docker-Client/19.03.12 \\(linux\\))"
```

Now we know exactly what happened to change the wishlist, we need to know how mayor malware managed to get access to upload anything. We will do this by heading back to our kubernetes environment.

```
kubectl get rolebindings -n wareville
```

There we see:

```
NAME                 ROLE              AGE
job-runner-binding   Role/job-runner   74d
mayor-user-binding   Role/mayor-user   74d
```

Now we will check further the rolebinding for mayor malware:

```
kubectl describe rolebinding mayor-user-binding -n wareville
```

From that we get the following information:

```
Name:         mayor-user-binding
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  Role
  Name:  mayor-user
Subjects:
  Kind  Name           Namespace
  ----  ----           ---------
  User  mayor-malware  
```

So we see that the user mayor-malware has the mayor-user-binding role. Now we will check the permissions under that role:

```
kubectl describe role mayor-user -n wareville
```

From that we receive:

```
Name:         mayor-user
Labels:       <none>
Annotations:  <none>
PolicyRule:
  Resources                               Non-Resource URLs  Resource Names  Verbs
  ---------                               -----------------  --------------  -----
  pods/exec                               []                 []              [create get list]
  rolebindings.rbac.authorization.k8s.io  []                 []              [get list describe]
  roles.rbac.authorization.k8s.io         []                 []              [get list describe]
  pods                                    []                 []              [get list watch]
```

Here we receive an unusual permission which is pods/exec which means that the user can access a shell in the containers in the pod.
Now we are able to access and check the logs specifically for the mayor malware user using the following command:

```
cat audit.log | grep --color=always '"user":{"username":"mayor-malware"' | grep --color=always '"resource"' | grep --color=always '"verb"'
```

After discovering all of the commands and the process that Mayor Malware took, we can now run the following command to discover the secret credentials:

```
kubectl get secret pull-creds -n wareville -o jsonpath='{.data.\.dockerconfigjson}' | base64 --decode
```

Receiving the following:

```
{"auths":{"http://docker-registry.nicetown.loc:5000":{"username":"mr.nice","password":"Mr.N4ughty","auth":"bXIubmljZTpNci5ONHVnaHR5"}}}
```