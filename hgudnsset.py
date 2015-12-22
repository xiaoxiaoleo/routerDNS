#!/usr/bin/env python
# coding=utf-8
# code by 92ez.com
# author kbdancer
# create time 2015-12-22

import Queue
from threading import Thread
import telnetlib
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
    hosts = iplist
    for host in hosts:
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
            except Exception,e:
                continue

def setDNS(host):

    username = "telnetadmin"
    password = "telnetadmin"

    # another account
    # username = "e8ehome"
    # password = "e8ehome"

    telnetTime = 5
    cmdTime = 5

    try:
        t = telnetlib.Telnet(host, timeout = telnetTime)
        t.read_until("Login: ", cmdTime)
        t.write(username + "\n")
        t.read_until("Password: ", cmdTime)
        t.write(password + "\n")
        t.read_until(" > ",cmdTime)
        t.write("?" + "\n")
        t.read_until("?",cmdTime)
        loginStr = t.read_very_eager()
        time.sleep(2)
        if len(loginStr)>100:

            t.write("dns config static "+ DNS1 +" "+ DNS2 +"\n")
            t.read_until(" > ",cmdTime)
            t.write("save\n")
            t.read_until("config",cmdTime)
            setResult = t.read_very_eager()
            t.close()

            if len(setResult)>0:
                print GetCurrentTime() +" IP:"+ host +" PORT:23 SET DNS SUCCESS !"
        else:
            t.close()
            return

    except Exception,e:
        return

if __name__ == '__main__':
    print '\n----------------------------------------\n'
    print '   SET DNS FOR HGU ROUTER BY PYTHON       '
    print '         http://www.92ez.com       '
    print '\n----------------------------------------\n'

    global SETTHREAD
    global DNS1
    global DNS2

    DNS1 = '114.114.114.114'
    DNS2 = '8.8.8.8'

    print "> DNS1 : "+DNS1
    print "> DNS2 : "+DNS2+"\n"

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