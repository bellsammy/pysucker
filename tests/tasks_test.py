# -*- coding: utf-8 -*-
import json
import os
import shutil
import time
import unittest

import lz4

from pysucker.default_config import RESSOURCES_PATH
from pysucker.robot import Robot, r, crawled_set, done_counter
from pysucker.tasks import crawl, parse, robot, count
from tests.samples.html_sample import html_sample


class CrawlTest(unittest.TestCase):

    def tearDown(self):
        try:
            shutil.rmtree(RESSOURCES_PATH)
        except OSError:
            pass

    def test_task_function(self):
        # OK
        result = crawl('http://httpstat.us/200', RESSOURCES_PATH)
        self.assertEqual(result, '{}/httpstat.us/200'.format(RESSOURCES_PATH))
        # Errors
        with self.assertRaises(ValueError):
            crawl('http://httpstat.us/500', RESSOURCES_PATH)
        with self.assertRaises(ValueError):
            crawl('http://a.com', RESSOURCES_PATH)

class ParseTest(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(RESSOURCES_PATH):
            os.makedirs(RESSOURCES_PATH)
        with open('{}/index.html.data'.format(RESSOURCES_PATH), 'w') as f:
            f.write(html_sample)
        with open('{}/index.html.meta'.format(RESSOURCES_PATH), 'w') as f:
            json.dump({'content-type': 'text/html',
                       'url': 'http://www.example.com'}, f)

    def tearDown(self):
        try:
            shutil.rmtree(RESSOURCES_PATH)
        except OSError:            pass

    def test_task_function(self):
        result = parse('{}/index.html'.format(RESSOURCES_PATH))
        self.assertEqual(len(result), 11)
        self.assertIn(u'http://www.example.com/file1.html', result)


class RobotTest(unittest.TestCase):
    
    def setUp(self):
        if not os.path.exists(RESSOURCES_PATH):
            os.makedirs(RESSOURCES_PATH)

    def tearDown(self):
        Robot.clean()
        try:
            shutil.rmtree(RESSOURCES_PATH)
        except OSError:
            pass

    def test_task_function(self):
        allowed_hosts = ['httpstat.us']
        base_urls = ['http://httpstat.us/200']
        Robot([], allowed_hosts)
        robot(base_urls)
        self.assertEqual(r.scard(crawled_set), 1)
        time.sleep(1)

class CountTest(unittest.TestCase):

    def tearDown(self):
        Robot.clean()

    def test_task_function(self):
        count()
        self.assertEqual(r.get(done_counter), '1')
        count()
        self.assertEqual(r.get(done_counter), '2')

