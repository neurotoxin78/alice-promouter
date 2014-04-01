#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import path
import logging
root_path = path.dirname(path.realpath(__file__))[:-6]
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import choice, randint
from time import sleep
from colorlog import ColoredFormatter
from ConfigParser import SafeConfigParser


logger = logging.getLogger('phantom')
hdlr = logging.FileHandler(root_path+'/alice-promo.log')
#formatter = logging.Formatter(u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')
formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-2s [%(asctime)s] %(filename)s %(reset)s %(yellow)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red',
        }
)

hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)



class phantom(object):

    """Docstring for phantom. """

    def __init__(self):
        """@todo: to be defined1. """
        self.cfg = SafeConfigParser()
    
    def get_random_ua(self):
        """@todo: Docstring for get_random_ua.
        :returns: @todo

        """
        with open(root_path+"/uas/uas.txt", "r") as f:
            ua_list = f.readlines()
        return choice(ua_list)

    def get_random_proxy(self):
        """@todo: Docstring for get_random_proxy.
        :returns: @todo

        """
        with open(root_path+"/lists/alive.list","r") as f:
            alive_list = f.readlines()
        
        return choice(alive_list)

    def visit(self,  url):
        """@todo: Docstring for visit.

        :url: @todo
        :returns: @todo

        """
        # Get proxy
        rproxy = self.get_random_proxy().split(':')
        service_args = ['--proxy='+rproxy[0]+':'+rproxy[1], '--proxy-type='+rproxy[2].replace('\n',''),]
        ## User-Agent
        ua = self.get_random_ua()
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (ua)


        driver = webdriver.PhantomJS(path=root_path+"/bin/_phantomjs", service_args=service_args, desired_capabilities=dcap) # or add to your PATH
        driver.set_window_size(1024, 768) # optional
        driver.set_page_load_timeout(15)
        driver.set_script_timeout(15)
        driver.get(url)
        #driver.save_screenshot(root_path+'/screenshots/screen_'+str(randint(0,65535))+'.png') # save a screenshot to disk
        driver.close()

    def walk(self,  project, chk_string):
        """@todo: Docstring for walk.

        :url: @todo
        :proxy: @todo
        :returns: @todo

        """
        proxy=self.get_random_proxy() 
        ua=self.get_random_ua()

        url_file = root_path+"projects/"+project+"/internal_urls"
        with open(url_file,'r') as f:
            url_list = f.readlines()

        ## Walk 
        for item in url_list:
            try:
                #print root_path 
                rproxy = proxy.split(':')
                service_args = ['--proxy='+rproxy[0]+':'+rproxy[1], '--proxy-type='+rproxy[2].replace('\n',''),]
                ## User-Agent
                dcap = dict(DesiredCapabilities.PHANTOMJS)
                dcap["phantomjs.page.settings.userAgent"] = (ua)
                driver = webdriver.PhantomJS(executable_path=root_path+"bin/_phantomjs", service_args=service_args, desired_capabilities=dcap) # or add to your PATH
                driver.set_window_size(1024, 768) # optional
                driver.set_page_load_timeout(15)
                driver.set_script_timeout(15)
                timewait = randint(10, 290)
                log = u'-> '+ item.replace('\n','') + ' via '+ str(service_args) + " : " + str(timewait)+u's'
                logger.info(log)                
                driver.get(item.replace('\n',''))
                logger.info(driver.title)
                if chk_string in driver.title:
                    logger.info('Ok')
                    sleep(timewait)
#                    try:
#                        driver.close()
#                    except:
#                        pass
                else:
                    logger.info('Wrong request: change proxy')
#                    try:
#                        driver.close()
#                    except:
#                        pass
                    ## Change proxy
#                    logger.error(u'Что то не так, меняю прокси')
                    proxy=self.get_random_proxy() 
                    ua=self.get_random_ua()
                    rproxy = proxy.split(':')
                    service_args = ['--proxy='+rproxy[0]+':'+rproxy[1], '--proxy-type='+rproxy[2].replace('\n',''),]
                    ## User-Agent
                    dcap = dict(DesiredCapabilities.PHANTOMJS)
                    dcap["phantomjs.page.settings.userAgent"] = (ua)
                    driver = webdriver.PhantomJS(executable_path=root_path+"bin/_phantomjs",service_args=service_args, desired_capabilities=dcap) # or add to your PATH
                    driver.set_window_size(1024, 768) # optional
                    driver.set_page_load_timeout(15)
                    driver.set_script_timeout(15)                 
            except:
#                try:
#                    driver.close()
#                except:
#                    pass
                ## Change proxy
                logger.error(u'Что то не так, меняю прокси')
                proxy=self.get_random_proxy() 
                ua=self.get_random_ua()
                rproxy = proxy.split(':')
                service_args = ['--proxy='+rproxy[0]+':'+rproxy[1], '--proxy-type='+rproxy[2].replace('\n',''),]
                ## User-Agent
                dcap = dict(DesiredCapabilities.PHANTOMJS)
                dcap["phantomjs.page.settings.userAgent"] = (ua)
                driver = webdriver.PhantomJS(executable_path=root_path+"bin/_phantomjs", service_args=service_args, desired_capabilities=dcap) # or add to your PATH
                driver.set_window_size(1024, 768) # optional
                driver.set_page_load_timeout(15)
                driver.set_script_timeout(15)                
        driver.close()

    def get_ctl(self,  project):
        """@todo: Docstring for get_ctl.

        :project: @todo
        :returns: @todo

        """
        _prj_ctl_ = root_path+"projects/"+project+"/control"
        run_file = _prj_ctl_ + "/run"
        with open(run_file, 'r') as f:
            state = f.read().replace('\n','')
        if state == 'True':
            return True
        else:
            return False

    def walk_forever(self, project):
        """@todo: Docstring for walk_forever.

        :arg1: @todo
        :returns: @todo

        """
        prj_path = root_path+"projects/"+project
        
        self.cfg.read(prj_path+"/project.conf")
        cfg_dict = dict(self.cfg._sections['global'])        
        
        chk_string = cfg_dict['chk_string']


        state = self.get_ctl(project)

        while state == True:
            self.walk(project, chk_string)
            state = self.get_ctl(project)
        return 0


if __name__ == '__main__':
    ph=phantom()
    #ph.get_random_ua()
    ph.walk_forever('svkvisa')

