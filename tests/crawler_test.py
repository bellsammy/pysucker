# -*- coding: utf-8 -*-
import json
import os
import shutil
import unittest

from pysucker.crawler import Crawler
from pysucker.default_config import RESSOURCES_PATH


class CrawlerTest(unittest.TestCase):

    def tearDown(self):
        try:
            shutil.rmtree(RESSOURCES_PATH)
        except OSError:
            pass

    def test_init(self):
        crawler = Crawler('http://httpstat.us/200', '/dev/null',
                          user_agent='No Agent', language='fr-FR')
        self.assertEqual(crawler.absolute_url, 'http://httpstat.us/200')
        self.assertEqual(crawler.ressources_dir, '/dev/null/httpstat.us')
        self.assertEqual(crawler.file_name, '200')
        self.assertEqual(crawler.request_headers['User-Agent'], 'No Agent')
        self.assertEqual(crawler.request_headers['Accept-Language'], 'fr-FR')

    def test_fetch_error(self):
        # No response
        crawler = Crawler('http://a.com',
                              '/dev/null', user_agent='No Agent', language='fr-FR')
        self.assertFalse(crawler.fetch())
        self.assertFalse(crawler.response)

    def test_fetch_200(self):
        for code in range(200, 207):
            crawler = Crawler('http://httpstat.us/{}'.format(code),
                              '/dev/null', user_agent='No Agent', language='fr-FR')
            self.assertTrue(crawler.fetch(), 'Code {}'.format(code))
            self.assertTrue(crawler.response, 'Code {}'.format(code))

    def test_fetch_300(self):
        for code in range(300, 308):
            crawler = Crawler('http://httpstat.us/{}'.format(code),
                              '/dev/null', user_agent='No Agent', language='fr-FR')
            self.assertTrue(crawler.fetch(), 'Code {}'.format(code))
            self.assertTrue(crawler.response, 'Code {}'.format(code))

    def test_fetch_400(self):
        for code in range(400, 418):
            crawler = Crawler('http://httpstat.us/{}'.format(code),
                              '/dev/null', user_agent='No Agent', language='fr-FR')
            self.assertTrue(crawler.fetch(), 'Code {}'.format(code))
            self.assertTrue(crawler.response, 'Code {}'.format(code))

    def test_fetch_500(self):
        for code in range(500, 506):
            crawler = Crawler('http://httpstat.us/{}'.format(code),
                              '/dev/null', user_agent='No Agent', language='fr-FR')
            self.assertFalse(crawler.fetch(), 'Code {}'.format(code))
            self.assertTrue(crawler.response, 'Code {}'.format(code))

    def test_url_to_filename(self):
        # Default
        crawler = Crawler('http://httpstat.us/', '/dev/null',
                          user_agent='No Agent', language='fr-FR')
        self.assertEqual(crawler.file_name, 'index.html')
        self.assertEqual(crawler.ressources_dir, '/dev/null/httpstat.us')
        # With args
        crawler = Crawler('http://httpstat.us/?test=1', '/dev/null',
                          user_agent='No Agent', language='fr-FR')
        self.assertEqual(crawler.file_name, 'index.html?test=1')
        self.assertEqual(crawler.ressources_dir, '/dev/null/httpstat.us')
        # With directories
        crawler = Crawler('http://httpstat.us/sub1/sub2/toto.php?test=1', '/dev/null',
                          user_agent='No Agent', language='fr-FR')
        self.assertEqual(crawler.file_name, 'toto.php?test=1')
        self.assertEqual(crawler.ressources_dir, '/dev/null/httpstat.us/sub1/sub2')

    def test_file_path(self):
        crawler = Crawler('http://httpstat.us/sub1/sub2/toto.php?test=1', '/dev/null',
                          user_agent='No Agent', language='fr-FR')
        self.assertEqual(crawler.file_path(), '/dev/null/httpstat.us/sub1/sub2/toto.php?test=1')

    def test_ensure_directory(self):
        crawler = Crawler('http://httpstat.us/sub1/sub2/toto.php?test=1', RESSOURCES_PATH,
                          user_agent='No Agent', language='fr-FR')
        crawler.ensure_directory()
        self.assertTrue(os.path.exists('{}/httpstat.us//sub1/sub2'.format(RESSOURCES_PATH)))

    def test_save(self):
        crawler = Crawler('http://httpstat.us/301', RESSOURCES_PATH,
                          user_agent='No Agent', language='fr-FR')
        if crawler.fetch():
            crawler.save()
        with open('{}/httpstat.us/301.data'.format(RESSOURCES_PATH), 'r') as f:
            ressource = f.read()
            self.assertIn('301 Moved Permanently', ressource)
        with open('{}/httpstat.us/301.meta'.format(RESSOURCES_PATH), 'r') as f:
            meta = json.loads(f.read())
            self.assertIn('text/plain', meta['content-type'])
            self.assertEqual('http://httpstat.us/301', meta['url'])
            self.assertEqual(301, meta['status'])
            self.assertEqual('http://httpstat.us', meta['location'])
        

