# -*- coding: utf-8 -*-
import shutil
import unittest

import lz4

from pysucker.crawler import Crawler


RESSOURCES_PATH = '/tmp/pysucker_test'


class CrawlerTest(unittest.TestCase):

    def tearDown(self):
        try:
            shutil.rmtree(RESSOURCES_PATH)
        except OSError:
            pass

    def test_init(self):
        crawler = Crawler('http://www.google.fr', '/dev/null', 'index.html',
                          user_agent='No Agent', language='fr-FR')
        self.assertEqual(crawler.absolute_url, 'http://www.google.fr')
        self.assertEqual(crawler.ressources_dir, '/dev/null')
        self.assertEqual(crawler.file_name, 'index.html')
        self.assertEqual(crawler.request_headers['User-Agent'], 'No Agent')
        self.assertEqual(crawler.request_headers['Accept-Language'], 'fr-FR')

    def test_fetch(self):
        # Valid URL
        crawler = Crawler('http://www.google.fr', '/dev/null', 'index.html',
                          user_agent='No Agent', language='fr-FR')
        self.assertTrue(crawler.fetch())
        # Unknow URL
        crawler = Crawler('http://www.google.fr/toto', '/dev/null', 'index.html',
                          user_agent='No Agent', language='fr-FR')
        self.assertFalse(crawler.fetch())

    def test_url_to_path(self):
        # Default
        crawler = Crawler('http://www.google.fr/', '/dev/null',
                          user_agent='No Agent', language='fr-FR')
        self.assertEqual(crawler.file_name, 'index.html')
        self.assertEqual(crawler.ressources_dir, '/dev/null')
        # With args
        crawler = Crawler('http://www.google.fr/?test=1', '/dev/null',
                          user_agent='No Agent', language='fr-FR')
        self.assertEqual(crawler.file_name, 'index.html?test=1')
        self.assertEqual(crawler.ressources_dir, '/dev/null')
        # With directories
        crawler = Crawler('http://www.google.fr/sub1/sub2/toto.php?test=1', '/dev/null',
                          user_agent='No Agent', language='fr-FR')
        self.assertEqual(crawler.file_name, 'toto.php?test=1')
        self.assertEqual(crawler.ressources_dir, '/dev/null/sub1/sub2')

    def test_save(self):
        crawler = Crawler('http://www.google.fr/', RESSOURCES_PATH,
                          user_agent='No Agent', language='fr-FR')
        if crawler.fetch():
            crawler.save()
        with open('{}/index.html.lz4'.format(RESSOURCES_PATH), 'r') as f:
            ressource = lz4.loads(f.read())
            self.assertIn('google', ressource)
        

