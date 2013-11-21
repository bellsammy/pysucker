# -*- coding: utf-8 -*-
import os
import shutil
import time
import unittest

from pysucker.default_config import RESSOURCES_PATH
from pysucker.robot import Robot, r, crawled_set


TEST_RESSOURCES_PATH = '{}/test'.format(RESSOURCES_PATH)


class RobotTest(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(TEST_RESSOURCES_PATH):
            os.makedirs(TEST_RESSOURCES_PATH)

    def tearDown(self):
        Robot.clean()
        try:
            pass
            #shutil.rmtree(TEST_RESSOURCES_PATH)
        except OSError:
            pass
    
    def test_init(self):
        allowed_hosts = ['httpstat.us']
        base_urls = ['http://httpstat.us/200']
        # Without allowed hosts
        robot = Robot(base_urls)
        self.assertFalse(robot.allowed_hosts)
        # With allowed hosts
        robot = Robot(base_urls, allowed_hosts)
        self.assertEqual(robot.allowed_hosts, allowed_hosts)
        self.assertEqual(robot.base_urls, base_urls)
        # With know allowed hosts
        robot = Robot(base_urls)
        self.assertEqual(robot.allowed_hosts, allowed_hosts)

    def test_filter_urls(self):
        allowed_hosts = ['httpstat.us']
        base_urls = ['http://httpstat.us/200']
        # No allowed hosts
        self.assertFalse(list(Robot.filter_urls(base_urls)))
        # Invalid host
        robot = Robot(base_urls, allowed_hosts)
        self.assertFalse(list(Robot.filter_urls(['http://www.invalid.com'])))
        # Valid host
        self.assertEqual(len(list(Robot.filter_urls(['http://httpstat.us/200']))), 1)
        # Already crawled
        r.sadd(crawled_set, 'http://httpstat.us/200')
        self.assertFalse(list(Robot.filter_urls(['http://httpstat.us/200'])), 1)

    def test_start(self):
        # Valid URL
        allowed_hosts = ['httpstat.us']
        base_urls = ['http://httpstat.us/200']
        robot = Robot(base_urls, allowed_hosts)
        robot.start()
        self.assertEqual(r.scard(crawled_set), 1)
        time.sleep(1)
        with open('{}/httpstat.us/200.data'.format(TEST_RESSOURCES_PATH), 'r') as f:
            ressource = f.read()
            self.assertIn('OK', ressource)
