#!/usr/bin/env python2.7
#coding=utf-8
'''
Created on 2018.4.4
@author: liugang
'''

import json
import urllib2
import sys
import codecs

zabbix_url = "http://*/zabbix/api_jsonrpc.php"
zabbix_header = {"Content-Type":"application/json"}
zabbix_user = "admin"
zabbix_password = "zabbix"
auth_code = "*"
filename="c:\monitor_list.csv"
priority_dict={0:"Not classified",1:"information",2:"warming",3:"average",4:"high",5:"disaster"}
status_dict = {0:"enable",1:"disable"}
groupsnum = 0
hostsnum = 0
num=0

def save_to_file(txt):
    with codecs.open(filename, 'a', encoding='utf-8') as f:
        f.writelines(txt)

def get_host_by_groupid(groupid):
    json_data_host = {
        "method":"host.get",
        "params":{
            "output":["hostid","name"],
            "groupids":groupid,
#             "filter":{
#                 "status":0
#                 },
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
    return response_host['result']
    
def get_item_by_hostid(hostid):
    json_data_item = {
        "method":"item.get",
        "params":{
            "hostids":hostid,
            "output":[
                "itemid",
                "name",
                "key_",
                "delay",
                "status"
            ],
            "selectApplications":"1",
            "selectTriggers":"1"
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
    return response_item['result']

def get_application_by_applicationid(applicationid):
    json_data_application = {
        "method":"application.get",
        "params":{
            "applicationids":applicationid,
            "output":[
                "hostid",
                "name"],
        },
    }

    json_data_application.update(json_base)

    get_application_data = json.dumps(json_data_application)
    request_application = urllib2.Request(zabbix_url,get_application_data)
    for key in zabbix_header:
        request_application.add_header(key,zabbix_header[key])
    result_application = urllib2.urlopen(request_application)
    response_application = json.loads(result_application.read())
    result_application.close()
    return response_application['result']

def get_trigger_by_itemid(itemid):
    json_data_trigger = {
        "method":"trigger.get",
        "params":{
            "itemids":itemid,
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
    return response_trigger['result']

json_base = {
    "jsonrpc":"2.0",
    "auth":auth_code,
    "id":1
}

json_data_group = {
    "method":"hostgroup.get",
    "params":{
        "output":["groupids","name"],
        "selectHosts":"1",
        "search":{
            "name":"GRP"
        },
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
except urllib2.URLError as e:
    if hasattr(e, 'reason'):
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    elif hasattr(e, 'code'):
        print 'The server could not fulfill the request.'
        print 'Error code: ', e.code
else:
    response_group = json.loads(result_group.read())
    result_group.close()
    
    for count in response_group['result']:
        if "VOICE" in count["name"]:
            pass
        else:
            groupsnum = groupsnum + 1
            hostsnum = hostsnum + len(count["hosts"])
    save_to_file("Total Group Num:"+str(groupsnum)+'\t' +"Total Hosts Num:" + str(hostsnum) +"\n")
    save_to_file("groupname"+"\t"+"hostname"+"\t"+"itemname"+"\t"+"application"+"\t"+"item_key"+"\t"+"interval"+"\t"+"item_status"+"\t"+"trigger_name"+"\t"+"trigger_expression"+"\t"+"Severity"+"\t"+"trigger_status"+"\n")
    for grouplist in response_group['result']:
        if "VOICE" in grouplist["name"]:
            pass
        else:
            save_to_file(grouplist["name"])
            print ("group:"+grouplist["name"])
            if len(grouplist['hosts']) == 0:
                save_to_file("There is no host in this group."+"\n")
            else:
                for hostlist in get_host_by_groupid(grouplist["groupid"]):
                    num = num + 1
                    save_to_file('\t'+hostlist["name"])
                    print ( "%d \t %s" %(num,hostlist["name"]))
                    itemlists = get_item_by_hostid(hostlist['hostid'])

                    if len(itemlists) == 0:
                        save_to_file("there is no item in this host."+"\n")
                    else :
                        if len(itemlists[0]['applications']) == 0:
                            application = "none"
                        else:
                            application = get_application_by_applicationid(itemlists[0]['applications'][0]["applicationid"])[0]["name"]
                            for applicationidlist in range(1,len(itemlists[0]['applications'])):
                                application = application + ',' + get_application_by_applicationid(itemlists[0]['applications'][applicationidlist]["applicationid"])[0]["name"]
                        save_to_file('\t'+itemlists[0]['name']+'\t'+application+'\t'+itemlists[0]['key_']+'\t'+itemlists[0]['delay']+'\t'+status_dict[int(itemlists[0]['status'])])
                        if len(itemlists[0]['triggers']) == 0:
                            save_to_file('\n')
                        else:
                            triggerlist=get_trigger_by_itemid(itemlists[0]['itemid'])
                            save_to_file('\t'+triggerlist[0]['description']+'\t'+triggerlist[0]['expression']+'\t'+priority_dict[int(triggerlist[0]["priority"])]+'\t'+status_dict[int(triggerlist[0]['status'])]+'\n')
                            for triggers in range(1,len(triggerlist)):
                                save_to_file('\t'+'\t'+'\t'+'\t'+'\t'+'\t'+'\t'+triggerlist[triggers]['description']+'\t'+triggerlist[triggers]['expression']+'\t'+priority_dict[int(triggerlist[triggers]["priority"])]+'\t'+status_dict[int(triggerlist[triggers]["status"])]+'\n')
            
                        for itemlist in range(1,len(itemlists)):
                            if len(itemlists[itemlist]['applications']) == 0:
                                application = "none"
                            else:
                                application = get_application_by_applicationid(itemlists[itemlist]['applications'][0]["applicationid"])[0]["name"]
                                for applicationidlist in range(1,len(itemlists[itemlist]['applications'])):
                                    application = application + ',' + get_application_by_applicationid(itemlists[itemlist]['applications'][applicationidlist]["applicationid"])[0]["name"]
                            save_to_file('\t'+'\t'+itemlists[itemlist]['name']+'\t'+application+'\t'+itemlists[itemlist]['key_']+'\t'+itemlists[itemlist]['delay']+'\t'+status_dict[int(itemlists[itemlist]['status'])])
                            if len(itemlists[itemlist]['triggers']) == 0:
                                save_to_file('\n')
                            else:
                                triggerlist=get_trigger_by_itemid(itemlists[itemlist]['itemid'])
                                save_to_file('\t'+triggerlist[0]['description']+'\t'+triggerlist[0]['expression']+'\t'+priority_dict[int(triggerlist[0]["priority"])]+'\t'+status_dict[int(triggerlist[0]['status'])]+'\n')
                                for triggers in range(1,len(triggerlist)):
                                    save_to_file('\t'+'\t'+'\t'+'\t'+'\t'+'\t'+'\t'+triggerlist[triggers]['description']+'\t'+triggerlist[triggers]['expression']+'\t'+priority_dict[int(triggerlist[triggers]["priority"])]+'\t'+status_dict[int(triggerlist[triggers]["status"])]+'\n')
                                    
