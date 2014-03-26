#!/usr/bin/python
# -*- coding: utf-8 -*-
from common.proxylist import proxy
from common.phantoms import phantom
from multiprocessing import Process

p=proxy()
# Make proxylist
p.make_proxy_lists()

f=phantom()
THREADS = 100



def worker():
    """@todo: Docstring for target.
    :returns: @todo

    """
    f.walk_forever('svkvisa')

if __name__ == '__main__':
    jobs = []
    for i in range(20):
        p = Process(target=worker)
        jobs.append(p)
        p.start()



