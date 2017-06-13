#!/usr/bin/env python2.7
#-*- coding=utf8 -*-
from pyzabbix import ZabbixAPI
from datetime import datetime
import time
import sys
class zabbix(object):
    def __init__(self,hostname,columns,name):
        self.hostname = hostname
        self.columns = columns
        self.dynamic = 0
        self.name = name
        self.server = 'http://192.168.52.129/zabbix'   #zabbix server ip
        self.user = 'admin'          #zabbix 帐号
        self.passwd = 'zabbix'       #密码
    def __login(self):          #登录
        zapi = ZabbixAPI(self.server)
        zapi.login(self.user,self.passwd)
        return zapi
    def __get_host(self): #获取主机
        list_host=self.__login().host.get(output='extend',filter={'host':self.hostname,})
#       print list_host
        return list_host[0]['hostid']
    def __get_item(self):   #主机对应的获取item
        list_item=self.__login().item.get(output='extend',hostids=self.__get_host())
        itemids=[]
        for x in list_item:
#           print x['name'],x['itemid']
            itemids.append(x['itemid'])
#       print itemids
        return itemids
    def __get_history(self):  #从历史中获取这些item判断是否有数据
        self.values={}
        for history  in  self.__get_item():
            list_history=self.__login().history.get(output='extend',itemids=history,limit=1)
#           print history
#           print list_history
            for point in list_history:     
#               print("{0}: {1}".format(datetime.fromtimestamp(int(point['clock'])).strftime("%x %X"), point['value']))
                if self.values.has_key(history):
                    self.values[history]=self.values[history]+int(point['value'])
                else:
                    self.values[history]=int(point['value'])
#           break
#       print self.values
    def __get_graph(self):  #获取绘图
        graphids=[]
        list_graph=self.__login().graph.get(output='extend',filter={"host":self.hostname})
        for x in list_graph:
            #print x['graphid']
            graphids.append(x['graphid'])
        print graphids
        return graphids
    def __get_graphitem(self): #从绘图中获取对应的item
        have_value_graph=[]
        for x in self.__get_graph():
#           print x
            list_graphitem=self.__login().graphitem.get(output='extend',graphids=x)
                                                                                                           
            have_value=[]
            for b in list_graphitem:
                number=len(list_graphitem)
                if b['itemid'] in self.values.keys():
                    if self.values[b['itemid']] != 0:
            #           print self.values[b['itemid']]
                        have_value.append(self.values[b['itemid']])
            if len(have_value) > 0:
                have_value_graph.append(x)
#       print have_value_graph
        x = 0
        y = 0
        graph_list=[]
        for graph in have_value_graph:
#           print "x is " + str(x)
#           print "y is " + str(y)
            graph_list.append({
                    "resourcetype":'0',
                    "resourceid": graph,
                    "width": "500",
                    "height": "100",
                    "x": str(x),
                    "y": str(y),
                    "colspan": "0",
                    "rowspan": "0",
                    "elements": "0",
                    "valign": "0",
                    "halign": "0",
                    "style": "0",
                    "url": "",
                    "dynamic": str(self.dynamic)
                    })
            x += 1
#           print type(x)
#           print type(self.columns)
            if x == int(self.columns):
                x = 0
                y += 1
        return graph_list
    def __create_screen(self):      #创建有数据的screen
        graphids=self.__get_graphitem()
        columns = int(self.columns)
        if len(graphids) % self.columns == 0:
            vsize = len(graphids) / self.columns
        else:
            vsize = (len(graphids) / self.columns) + 1
#       print graphids
        self.__login().screen.create(name=self.name,hsize=self.columns,vsize=vsize,screenitems=graphids)
    def __exists_screen(self):
        list_exists=self.__login().screen.exists(name=self.name)
        if list_exists:
            print '%s is exists' % self.name
            sys.exit(1)
    def __exists_host(self):
        list_exists=self.__login().host.exists(host=self.hostname)
        if not list_exists:
            print "%s is not exists" % self.hostname
    def main(self):
        self.__exists_host()
        self.__exists_screen()
#       self.__get_host()
#       self.__get_item()  
        self.__get_history()
#       self.__get_graph()
#       self.__get_graphitem()
        self.__create_screen()
if __name__ == '__main__':
    from  optparse import OptionParser  #帮助
    parser = OptionParser()
    parser.add_option('-G', dest='graphname',
                        help='Zabbix Host Graph to create screen from')
    parser.add_option('-H', dest='hostname',
                        help='Zabbix Host to create screen from')
    parser.add_option('-c', dest='columns', type=int,
                        help='number of columns in the screen')
    options,args=parser.parse_args()
#   print options.columns
#   print options.hostname,options.columns,options.graphname
    a=zabbix(hostname=options.hostname,columns=options.columns,name=options.graphname)
    a.main()
