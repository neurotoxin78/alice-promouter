#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import path, listdir
import logging
from colorlog import ColoredFormatter
from common.phantoms import phantom
root_path = path.dirname(path.realpath(__file__))
from multiprocessing import Process
from ConfigParser import SafeConfigParser

logger = logging.getLogger('project')
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


class project(object):

    """Docstring for project. """

    def __init__(self):
        """@todo: to be defined1. """
        self.f = phantom()
        self.cfg = SafeConfigParser()
    
    def worker(self, prj_name):
        """@todo: Docstring for run.
        :returns: @todo

        """
        #pf = root_path+'/projects'
        #print listdir(pf)
        
        self.f.walk_forever(prj_name)
        
    
    def run_project(self, prj_name):
        """@todo: Docstring for run_project.

        :prj_name: @todo
        :returns: @todo

        """
        prj_path = root_path+"/projects/"+prj_name   
        self.cfg.read(prj_path+"/project.conf")
        cfg_dict = dict(self.cfg._sections['global'])
        threads = int(cfg_dict['run_instances'])
        jobs = []
        for i in range(threads):
            print prj_name
            p = Process(target=self.worker, args=[prj_name])
            jobs.append(p)
            p.start()


        
    
    def run_all(self):
        """@todo: Docstring for run_all.
        :returns: @todo

        """
        jobs = []
        prj_path = root_path+"/projects/"
        projects = listdir(prj_path)
        print projects
        for item in projects:
            p = Process(target=self.run_project, args=[item])
            jobs.append(p)
            p.start()
            
            #self.run_project(item)



if __name__ == '__main__':
    p=project()
#    p.run_project('svkvisa')
    p.run_all()




