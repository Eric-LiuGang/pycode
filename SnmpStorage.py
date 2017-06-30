#!/usr/bin/env python2.7
#coding=utf-8
import sys
import xlsxwriter
from urllib import urlopen
from xml.etree.ElementTree import parse

u=urlopen('http://monitor.iv-cloud.com/iconnector/servlet/snmpmonitorservlet?serverId=00021&getDeviceData=true')
doc=parse(u)

workbook = xlsxwriter.Workbook('C:\Users\liugang\Desktop\storage.xlsx')
worksheet = workbook.add_worksheet('storage')
row=1
col=1

worksheet.write(1,1,'eqliscsiVolumeName')
worksheet.write(1,2,'eqliscsiVolumeSize')
worksheet.write(1,3,'reserved')
worksheet.write(1,5,'eqliscsiVolumeStatusAllocatedpercentaged')
worksheet.write(1,6,'WarnPercentage')
worksheet.write(1,8,'eqliscsiVolumeStatusReservedSpace')
worksheet.write(1,9,'eqliscsiVolumeStatusReservedSpaceAvail')
worksheet.write(1,10,'eqliscsiVolumeSnapWarningLevel')
worksheet.write(1,11,'eqliscsiVolumeStatusReplReserveSpace')
worksheet.write(1,12,'eqliscsiVolumeStatusAllocatedSpace')

for SnmpDeviceDate in doc.iter('SnmpDeviceData'):
    devicename          =SnmpDeviceDate.get('deviceName')
    volumename          =SnmpDeviceDate.get('eqliscsiVolumeName')
    category            =SnmpDeviceDate.get('eqliscsiVolumeStoragePoolIndex')
    size                =SnmpDeviceDate.get('eqliscsiVolumeSize')
    thinprovision       =SnmpDeviceDate.get('eqliscsiVolumeThinProvision')
    thinreserve         =SnmpDeviceDate.get('eqliscsiVolumeDynamicThinReserve')
    allocated           =SnmpDeviceDate.get('eqliscsiVolumeStatusAllocatedSpace')
    warnpercentage      =SnmpDeviceDate.get('eqliscsiVolumeThinWarnPercentage')
    statusreserved      =SnmpDeviceDate.get('eqliscsiVolumeStatusReservedSpace')
    statusreservedavail =SnmpDeviceDate.get('eqliscsiVolumeStatusReservedSpaceAvail')
    snapwarninglevel    =SnmpDeviceDate.get('eqliscsiVolumeSnapWarningLevel')
    replreserve         =SnmpDeviceDate.get('eqliscsiVolumeStatusReplReserveSpace')


    if devicename == 'LWSEQDATA' and size!=None and size!='0':
        col=1
        row=row+1
        worksheet.write(row,col,volumename)
        col=col+1
        worksheet.write(row,col,float(size)/1024)
        col=col+1
        if thinprovision==2:
            worksheet.write(row,col,float(size)/1024)
            col =col+1
        elif thinreserve==None:
            worksheet.write(row,col,0)
            col =col+1
        else:
            worksheet.write(row,col,float(thinreserve)/1024)
            col =col+1
        worksheet.write(row,col,(1-float(allocated)/int(size)))
        col=col+1
        worksheet.write(row,col,float(allocated)/int(size))
        col=col+1
        worksheet.write(row,col,int(warnpercentage))
        col =col+2
        worksheet.write(row,col,int(statusreserved)/1024)
        col=col+1
        worksheet.write(row,col,(int(statusreserved)/1024-int(statusreservedavail)/1024))
        col=col+1
        worksheet.write(row,col,float(snapwarninglevel)/100)
        col=col+1
        worksheet.write(row,col,float(replreserve)/1024)
        col=col+1
        worksheet.write(row,col,float(allocated)/1024)
    
workbook.close()
                                                       
        