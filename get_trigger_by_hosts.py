#!/usr/bin/env python2.7
#coding=utf-8
import json
import urllib2
import sys
from urllib2 import Request,urlopen,URLError,HTTPError


zabbix_url = "http://*/zabbix/api_jsonrpc.php"
zabbix_header = {"Content-Type":"application/json"}
zabbix_user = "admin"
zabbix_password = "zabbix"
auth_code = ""

#step 1 get all host which status 0

f=open('C:\*','w')
#step 1 get all host which status 0
json_base = {
    "jsonrpc":"2.0",
    "auth":auth_code, # theauth id is what auth script returns, remeber it is string
    "id":1,
}
 
json_data = {
    "method":"host.get",
    "params":{
        "output":[
            "host",
            "name",
            "hostid",
        ],
    "filter":{
        "status":0
        },
    },
}
 
json_data.update(json_base)
 
if len(auth_code) == 0:
    sys.exit(1)
 
if len(auth_code) != 0:
    get_host_data = json.dumps( json_data )
    request_host = urllib2.Request(zabbix_url,get_host_data)
    for key in zabbix_header:
        request_host.add_header(key,zabbix_header[key])
         
 
# get host list from request
try:
    result_host = urllib2.urlopen(request_host)
except URLError as e:
    if hasattr(e, 'reason'):
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    elif hasattr(e, 'code'):
        print 'The server could not fulfill the request.'
        print 'Error code: ', e.code
else:
    response_host = json.loads(result_host.read())
    result_host.close()
 
    print "Number Of result: ", len(response_host['result'])
    f.write("Number Of result: "+str(len(response_host['result']))+'\n') 
    for hostlist in response_host['result']:
        print hostlist['host'],"\t"
        f.write(hostlist['host']+'\n')
        hostid =  hostlist['hostid'].encode("utf-8")
         
        json_data = {
            "method":"trigger.get",
            "params":{
                "output":[
                    "description"
                ],
                "hostids":"10098",
                "status":"0"
            },
        }
        
        json_data.update(json_base)
        
        get_trigger_data = json.dumps(json_data)
        request_trigger = urllib2.Request(zabbix_url,get_trigger_data)
        for key in zabbix_header:
            request_trigger.add_header(key,zabbix_header[key])
        result_trigger = urllib2.urlopen(request_trigger)
        response_trigger = json.loads(result_trigger.read())
        result_trigger.close()
        for triggerlist in response_trigger['result']:
            print "\t",triggerlist['description']
            f.write('\t'+str(triggerlist['description'])+'\n')
f.close()
