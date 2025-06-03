# cURL

### Basic Commands:

**cURL Help Menu**

```
curl -h
```

**Basic GET Request**

```
curl inlanefreight.com
```

**Download File**

```
curl -s -O inlanefreight.com/index.html
```

**Skip HTTPS (SSL)**

```
curl -k https://inlanefreight.com
```

**Print full HTTP Request/Response**

```
curl inlanefreight.com -v
```

**Send HEAD Request (only response headers)**

```
curl -I https://www.inlanefreight.com
```

**Print Response Headers and Body**

```
curl -i https://www.inlanefreight.com
```

**Set User-Agent Header**

```
curl https://www.inlanefreight.com -A 'Mozilla/5.0'
```

**Set HTTP Basic Authorisation Credentials**

```
curl -u admin:admin https://<SERVER_IP>:<PORT>/
```

**Pass HTTP Basic Authorisation Credentials in URL**

```
curl http://admin:admin@<SERVER_IP>:<PORT>/
```

**Set Request Header**

```
curl -H 'Authorisation: Basic YWRtaW46YWRtaW4=' http://<SERVER_IP>:<PORT>/
```

**Pass GET Parameters**

```
curl 'http://<SERVER_IP>:<PORT>/search.php?search=le'
```

**Send POST Request with POST Data**

```
curl -X POST -d 'username=admin&password=admin' http://<SERVER_IP>:<PORT>/
```

**Set Request Cookies**

```
curl -b 'PHPSESSID=clnsa6op7vtk7kdis7bcnbadf1' http://<SERVER_IP>:<PORT>/
```

**Send POST Request with JSON Data**

```
curl -X POST -d '{"search":"london"}' -H 'Content-Type: application/json' http://<SERVER_IP>:<PORT>/search.php
```

### API Commands

**Read Entry**

```
curl http://<SERVER_IP>:<PORT>/api.php/city/london
```

**Read All Entries**

```
curl -s http://<SERVER_IP>:<PORT>/api.php/city/ | jq
```

**Create (Add) Entry**

```
curl -X POST http://<SERVER_IP>:<PORT>/api.php/city/ -d '{"city_name":"HTB_City", "country_name":"HTB"}' -H 'Content-Type: application/json'
```

**Update (Modify) Entry**

```
curl -X PUT http://<SERVER_IP>:<PORT>/api.php/city/london -d '{"city_name":"New_HTB_City", "country_name":"HTB"}' -H 'Content-Type: application/json'
```

**Delete Entry**
```
curl -X DELETE http://<SERVER_IP>:<PORT>/api.php/city/New_HTB_City
```