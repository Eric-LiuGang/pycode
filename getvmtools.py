#!/usr/bin/env python2.7
#coding=utf-8
import json
import urllib2
import sys
from urllib2 import Request,urlopen,URLError,HTTPError


zabbix_url = "http://192.168.52.129/zabbix/api_jsonrpc.php"
zabbix_header = {"Content-Type":"application/json"}
zabbix_user = "admin"
zabbix_password = "zabbix"
auth_code = "25d5dc7f328864a845bb36f731f79017"
auth_data = json.dumps(
{
   "jsonrpc": "2.0",
   "method": "user.login",
   "params": {
   "user": zabbix_user,
   "password": zabbix_password
},
"id": 0,
})
# create request object
request = urllib2.Request(zabbix_url,auth_data)
for key in zabbix_header:
    request.add_header(key,zabbix_header[key])
# auth and get authid
try:
    result = urllib2.urlopen(request)
except HTTPError as e:
    print "tHE SERVER COULDN\'T FULFILL THE REQUEST, ERROR CODE: ",e.code
except URLError as e:
    print "WE FAILED TO REACH A SERVER.REASON: ",e.reason
else:
    response = json.loads(result.read())
    result.close()
    if 'result' in response:
        print"Auth Successful. The Auth ID Is:",response['result']
    else:
        print response['error']['data']
