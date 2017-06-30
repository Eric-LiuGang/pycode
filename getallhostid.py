#!/usr/bin/env python2.7
#coding=utf-8
import json
import urllib2
import sys
from urllib2 import Request,urlopen,URLError,HTTPError


zabbix_url = "http://172.31.2.121/zabbix/api_jsonrpc.php"
zabbix_header = {"Content-Type":"application/json"}
zabbix_user = "admin"
zabbix_password = "zabbix"
auth_code = ""

# NEW AUTH_CODE GET
'''
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
'''

# request json
json_data = {
    "method":"host.get",
    "params":{
        "output":"extend",
        "filter":{
            "status":"0"
            },
    },
}
json_base = {
    "jsonrpc":"2.0",
    "auth":auth_code, # theauth id is what auth script returns, remeber it is string
    "id":1,
}

json_data.update(json_base)

if len(auth_code) == 0:
    sys.exit(1)

if len(auth_code) != 0:
    get_host_data = json.dumps( json_data)
    request = urllib2.Request(zabbix_url,get_host_data)
    for key in zabbix_header:
        request.add_header(key,zabbix_header[key])
        

# get host list from request
try:
    result = urllib2.urlopen(request)
except URLError as e:
    if hasattr(e, 'reason'):
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    elif hasattr(e, 'code'):
        print 'The server could not fulfill the request.'
        print 'Error code: ', e.code
else:
    response = json.loads(result.read())
    result.close()
#    print response
    print "Number Of result: ", len(response['result'])
    #print response
    i=1
    for line in response['result']:
            print i,"\thost: \t",line['host'],"\tname: \t",line['name'],"\thostid: \t",line['hostid']
            i=i+1
