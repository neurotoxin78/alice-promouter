#!/usr/bin/python
# -*- coding: utf-8 -*-
from grab import Grab, GrabError
from os import path, mkdir
root_path = path.dirname(path.realpath(__file__))[:-6]
    
class project(object):

    """Docstring for project. """

    def __init__(self):
        """@todo: to be defined1. """

    def remove_duplicates(self, url_list):
        """@todo: Docstring for remove_duplicates.

        :list: @todo
        :returns: @todo

        """
        return list(set(url_list))

    def get_site_links(self, url):
        """@todo: Docstring for get_site_links.

        :arg1: @todo
        :returns: @todo

        """
        g=Grab()
        g.go(url)
        links = g.xpath_list('//a')
        url_list = []
        for i in links:
            url_list.append(i.get('href'))
        
        return self.remove_duplicates(url_list)

    def make_internal_url_list(self,  url):
        """@todo: Docstring for make_internal_url_list.

        :url: @todo
        :returns: @todo

        """
        url_list = self.get_site_links(url)
#        print url_list

        iurl_list=[]
        for i in url_list:
            if type(i) == str:
                if i.find('http') == -1:
                    if i.find('#') == -1:
                        iurl_list.append(url+i)
        return iurl_list 
    
    def mkproject(self, name, url):
        """@todo: Docstring for mkproject.

        :name: @todo
        :url: @todo
        :returns: @todo

        """
        ## Make dir
        prj_path = root_path+"projects/"+name
        try:
            mkdir(prj_path)
        except:
            print 'Allredy exist'
        
        url_list = self.make_internal_url_list(url)
        with open(prj_path+'/internal_urls','w') as f:
            for i in url_list:
                f.write(i+'\n')


if __name__ == '__main__':
    p=project()
    print p.mkproject('svkvisa','http://svk-visa.com')

