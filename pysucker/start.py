# -*- coding: utf-8 -*-
import importlib
import time
import datetime
from robot import Robot, allowed_hosts_set, crawled_set, done_counter, r
from tasks import app
from collections import Counter
from celery.task.control import inspect


base_urls = 'http://httpstat.us'
allowed_hosts = 'httpstat.us'
robot = Robot(base_urls, allowed_hosts)
robot.clean()
robot = Robot(base_urls, allowed_hosts)
robot.start()

while True:
    print datetime.datetime.now(), 'Ressources: {}/{}'.format(r.get(done_counter) ,r.scard(crawled_set))
    # i = inspect()
    # counter = Counter()
    # for worker, tasks in i.active().iteritems():
    #     counter.update([task['name'] for task in tasks])
    # for worker, tasks in i.scheduled().iteritems():
    #     counter.update([task['name'] for task in tasks])
    # print counter.most_common()
    time.sleep(5)