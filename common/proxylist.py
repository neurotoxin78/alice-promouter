#!/usr/bin/python
# -*- coding: latin1 -*-
from grab import Grab, GrabError
from os import path, unlink
import subprocess
import logging
#logging.disable(logging.ERROR)

root_path = path.dirname(path.realpath(__file__))[:-6]
tmp = root_path+"tmp/"

class proxy(object):

    """Docstring for proxy. """

    def __init__(self):
        """@todo: to be defined1. """
    
    def make_proxy_lists(self):
        """@todo: Docstring for make_alive.
        :returns: @todo

        """
        self.get_proxy_premium()
        alive_list =  self.get_valid_proxy(root_path+'/lists/proxy.list')

        with open(root_path+'/lists/alive.list', 'w') as f:
            for i in alive_list:
                print i
                f.write(i+'\n')

        

    def get_valid_proxy(self, proxy_list): #format of items e.g. '128.2.198.188:3124'
        with open(proxy_list,'r') as f:
            proxy_list=f.readlines()
        g = Grab()
        for proxy in proxy_list:
            g.setup(proxy=proxy, proxy_type='http', connect_timeout=1, timeout=5)
            try:
                g.go('google.com', timeout=10)
            except GrabError:
                pass 
            else:
                try:
                    if g.xpath_list('//title')[0].text == u'Google':
                        print g.xpath_list('//title')[0].text
                        yield proxy.replace('\n','')+":http"
                except:
                    print "Bad proxy" 
    
    def get_proxy_premium(self,  code='989570157'):
        """@todo: Docstring for get_proxy_premium.

        :code: @todo
        :returns: @todo

        """
        g=Grab()
        g.go('http://hideme.ru/api/proxylist.php?country=ALAMAUBEBGCACZEEFRGEDEILITKZLVMDNLANPLRORUCHTRUAGBUS&type=h&anon=1234&out=plain&code='+code)
        jlist = g.response.body.split()
        print jlist
        with open(root_path+'/lists/alive.list','w') as f: 
            for proxy in jlist:
                f.write(proxy+":http\n")





    def get_list(self):
        """@todo: Docstring for get_list.
        :returns: @todo

        """
        g=Grab()
        g.go('http://hideme.ru/proxy-list/?country=AMAZBEBGCAHRCZDKEEFRGEDEITKZLVLUMDNLPLRORURSSECHTRUAGBUS&type=h&anon=234&code=989570157')
        #print g.xpath_text('//table')
        ips = g.css_list('td.tdl')
        imgs = g.xpath_list('//td/img')

        c = 0
        srclist=[]
        for i in imgs:
            if c >= 5:
                srclist.append("http://hideme.ru"+i.attrib['src'])
            c+=1

        iplist=[]
        for ip in ips:
             iplist.append(ip.text)

        d={}
        c=0
        for i in range(len(iplist)):
            d[iplist[c]]=srclist[c]
            c+=1

        for k,v in d.items():
            subprocess.call('wget '+v+' -q -P '+tmp, shell=True)

        dt={}
        for k,v in d.items():
            cmdline = 'convert '+tmp+v[24:]+" "+tmp+v[24:-4]+'.pnm'
            ocrline = ['ocrad', '--filter=numbers_only', tmp+v[24:-4]+'.pnm']
            subprocess.call(cmdline, shell=True)
            unlink(tmp+v[24:])
            process = subprocess.Popen(ocrline, stdout=subprocess.PIPE)
            out, err = process.communicate()
            dt[k]=out.replace('\n\n','')
            unlink(tmp+v[24:-4]+'.pnm')

        ## Save proxy list
        with open(root_path+'lists/proxy.list','w') as f:
            for k,v in dt.items():
                f.write(k+":"+v+"\n")


if __name__ == '__main__':
    p=proxy()
#    p.make_proxy_lists()
    p.get_proxy_premium()
