#!/usr/bin/env python2.7
#coding=utf-8
'''
Created on 2017.9.7

@author: liugang
'''

import json
import urllib2
import sys
from urllib2 import Request,urlopen,URLError,HTTPError

#variable

zabbix_url = "http://172.17.254.20/zabbix/api_jsonrpc.php"
zabbix_header = {"Content-Type":"application/json"}
zabbix_user = "admin"
zabbix_password = "zabbix"
groupname="Glico_Wechat"
auth_code = "92c76072ed0acb629fc383e825051c2d"
f=open('C:\host_items.csv','w')
priority_dict={0:"Not classified",1:"information",2:"warming",3:"average",4:"high",5:"disaster"}
status_dict = {0:"enable",1:"disable"}
groupids=[]

#step 1 get groupid create groupids list with error verification

json_base = {
    "jsonrpc":"2.0",
    "auth":auth_code,
    "id":1
}

json_data_group = {
    "method":"hostgroup.get",
    "params":{
        "output":"groupids",
        "filter":{
            "name":groupname
        }
    },
}

json_data_group.update(json_base)

if len(auth_code) == 0:
    sys.exit(1)

if len(auth_code) != 0:
    get_group_data = json.dumps(json_data_group)
    request_group = urllib2.Request(zabbix_url,get_group_data)
    for key in zabbix_header:
        request_group.add_header(key,zabbix_header[key])

try:
    result_group = urllib2.urlopen(request_group)
except URLError as e:
    if hasattr(e, 'reason'):
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    elif hasattr(e, 'code'):
        print 'The server could not fulfill the request.'
        print 'Error code: ', e.code
else:
    response_group = json.loads(result_group.read())
    result_group.close()
    for grouplist in response_group['result']:
        groupids.append(int(grouplist["groupid"]))

#step 2 get all hostids from groupids

json_data_host = {

    "method":"host.get",
    "params":{
        "output":["hostid","name"],
        "groupids":groupids
    },
    "id":1,
}

json_data_host.update(json_base)


get_host_data = json.dumps( json_data_host )
request_host = urllib2.Request(zabbix_url,get_host_data)
for key in zabbix_header:
    request_host.add_header(key,zabbix_header[key])

result_host = urllib2.urlopen(request_host)
response_host = json.loads(result_host.read())
result_host.close()

print "Number Of Hosts: ", len(response_host['result'])
f.write("Number Of Hosts: "+str(len(response_host['result']))+'\n') 
f.write("hostname"+"\t"+"itemname"+"\t"+"item_key"+"\t"+"interval"+"\t"+"item_status"+"\t"+"trigger_name"+"\t"+"trigger_expression"+"\t"+"Severity"+"\t"+"trigger_status"+"\n")
for host in response_host['result']:
    f.write(host['name']),
    hostid =  host['hostid'].encode("utf-8")
    print hostid

#step 3 get all hitems from every host

    json_data_item = {
        "method":"item.get",
        "params":{
            "hostids":hostid,
            "selectTriggers":"",
            "output":[
                "itemid",
                "name",
                "key_",
                "delay",
                "status"
            ],
        },
    }

    json_data_item.update(json_base)

    get_item_data = json.dumps(json_data_item)
    request_item = urllib2.Request(zabbix_url,get_item_data)
    for key in zabbix_header:
        request_item.add_header(key,zabbix_header[key])
    result_item = urllib2.urlopen(request_item)
    response_item = json.loads(result_item.read())
    result_item.close()

    for itemlist in response_item['result']:
        f.write("\t"+itemlist["name"]+"\t"+itemlist["key_"]+"\t"+itemlist["delay"]+"\t"+status_dict[int(itemlist["status"])]+"\t"),
        
#step 4 get triggers with item
        
        if len(itemlist["triggers"]) ==0:
            f.write('\n')
        elif len(itemlist["triggers"]) ==1:
            triggerid=itemlist["triggers"][0]
            json_data_trigger = {
                "method":"trigger.get",
                "params":{
                    "triggerids":triggerid,
                    "expandExpression":"",
                    "output":[
                        "description",
                        "expression",
                        "priority",
                        "status"
                        ]
                },
            }
             
            json_data_trigger.update(json_base)
             
            get_trigger_data = json.dumps(json_data_trigger)
            request_trigger = urllib2.Request(zabbix_url,get_trigger_data)
            for key in zabbix_header:
                request_trigger.add_header(key,zabbix_header[key])
            result_trigger = urllib2.urlopen(request_trigger)
            response_trigger = json.loads(result_trigger.read())
            result_trigger.close()
            for triggerlist in response_trigger['result']:
                f.write(triggerlist["description"]+"\t"+triggerlist["expression"]+"\t"+priority_dict[int(triggerlist["priority"])]+"\t"+status_dict[int(triggerlist["status"])]+"\n")
        else:
            i=len(itemlist["triggers"])
            json_data_trigger = {
                "method":"trigger.get",
                "params":{
                    "triggerids":itemlist["triggers"][0],
                    "expandExpression":"",
                    "output":[
                        "description",
                        "expression",
                        "priority",
                        "status"
                        ]
                },
            }
             
            json_data_trigger.update(json_base)
             
            get_trigger_data = json.dumps(json_data_trigger)
            request_trigger = urllib2.Request(zabbix_url,get_trigger_data)
            for key in zabbix_header:
                request_trigger.add_header(key,zabbix_header[key])
            result_trigger = urllib2.urlopen(request_trigger)
            response_trigger = json.loads(result_trigger.read())
            result_trigger.close()
            for triggerlist in response_trigger['result']:
                f.write(triggerlist["description"]+"\t"+triggerlist["expression"]+"\t"+priority_dict[int(triggerlist["priority"])]+"\t"+status_dict[int(triggerlist["status"])]+"\n")
            for j in [1,i-1]:
                json_data_trigger = {
                    "method":"trigger.get",
                    "params":{
                        "triggerids":itemlist["triggers"][j],
                        "expandExpression":"",
                        "output":[
                            "description",
                            "expression",
                            "priority",
                            "status"
                            ]
                    },
                }

                json_data_trigger.update(json_base)
                get_trigger_data = json.dumps(json_data_trigger)
                request_trigger = urllib2.Request(zabbix_url,get_trigger_data)
                for key in zabbix_header:
                    request_trigger.add_header(key,zabbix_header[key])
                result_trigger = urllib2.urlopen(request_trigger)
                response_trigger = json.loads(result_trigger.read())
                result_trigger.close()
                for triggerlist in response_trigger['result']:
                    f.write("\t"+"\t"+"\t"+"\t"+"\t"+triggerlist["description"]+"\t"+triggerlist["expression"]+"\t"+priority_dict[int(triggerlist["priority"])]+"\t"+status_dict[int(triggerlist["status"])]+"\n")

f.close()
