# -*- coding: utf-8 -*-
import json
import os
import shutil
import unittest

from pysucker.parser import Parser, HtmlParser, CssParser, JavascriptParser
from pysucker.default_config import RESSOURCES_PATH
from tests.samples.html_sample import html_sample
from tests.samples.css_sample import css_sample
from tests.samples.js_sample import js_sample


class ParserTest(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(RESSOURCES_PATH):
            os.makedirs(RESSOURCES_PATH)

    def tearDown(self):
        try:
            shutil.rmtree(RESSOURCES_PATH)
        except OSError:
            pass

    def test_new(self):
        # Default with unknow html file.
        parser = Parser('{}/no_file.html'.format(RESSOURCES_PATH))
        self.assertIsInstance(parser, Parser)

    def test_load(self):
        # Default with unknow html file.
        content, meta = Parser.load('{}/no_file.html'.format(RESSOURCES_PATH))
        self.assertEqual(content, '')
        self.assertEqual(meta, {})
        # Existing file.__class__
        with open('{}/file.data'.format(RESSOURCES_PATH), 'w') as f:
            f.write('<h1>My Content</h1>')
        content, meta = Parser.load('{}/file'.format(RESSOURCES_PATH))
        self.assertEqual(content, '<h1>My Content</h1>')
        self.assertEqual(meta, {})

    def test_get_ressources(self):
        parser = Parser('{}/no_file.html'.format(RESSOURCES_PATH))
        self.assertFalse(len(list(parser.get_ressources())))
        self.assertFalse(len(list(parser.get_absolute_urls())))

    def test_html(self):
        file_name = '{}/file'.format(RESSOURCES_PATH)
        with open('{}.meta'.format(file_name), 'w') as f:
            json.dump({'content-type': 'text/html',
                       'url': 'http://www.example.com'}, f)
        parser = Parser(file_name)
        self.assertIsInstance(parser, HtmlParser)
        self.assertEqual(parser.source, 'http://www.example.com')

    def test_css(self):
        file_name = '{}/file'.format(RESSOURCES_PATH)
        with open('{}.meta'.format(file_name), 'w') as f:
            json.dump({'content-type': 'text/css',
                       'url': 'http://www.example.com'}, f)
        parser = Parser(file_name)
        self.assertIsInstance(parser, CssParser)
        self.assertEqual(parser.source, 'http://www.example.com')

    def test_js(self):
        file_name = '{}/file'.format(RESSOURCES_PATH)
        with open('{}.meta'.format(file_name), 'w') as f:
            json.dump({'content-type': 'text/javascript',
                       'url': 'http://www.example.com'}, f)
        parser = Parser(file_name)
        self.assertIsInstance(parser, JavascriptParser)
        self.assertEqual(parser.source, 'http://www.example.com')

class TestHtmlParser(unittest.TestCase):

    def setUp(self):
        self.parser = HtmlParser(html_sample, 'http://www.example.com')

    def tearDown(self):
        pass

    def test_get_images(self):
        links = list(self.parser.get_images())
        self.assertEqual(len(links), 2)
        self.assertIn('/image1.png', links)
        self.assertIn('/image2.png', links)

    def test_get_scripts(self):
        links = list(self.parser.get_scripts())
        self.assertEqual(len(links), 2)
        self.assertIn('/script1.js', links)
        self.assertIn('/script2.js', links)

    def test_get_links(self):
        links = list(self.parser.get_links())
        self.assertEqual(len(links), 5)
        self.assertIn('/favicon.ico', links)
        self.assertIn('/apple-touch-icon.png', links)
        self.assertIn('/apple-touch-icon.png', links)
        self.assertIn('/file1.html', links)
        self.assertIn('/file2.html', links)

    def test_parse_inline_css(self):
        links = list(self.parser.parse_inline_css())
        self.assertEqual(len(links), 1)
        self.assertIn('/background.png', links)

    def test_parse_inline_scripts(self):
        links = list(self.parser.parse_inline_scripts())
        self.assertEqual(len(links), 1)
        self.assertIn('/inline-js-file.html', links)

    def test_get_ressources(self):
        links = list(self.parser.get_ressources())
        self.assertEqual(len(links), 11)
        self.assertIn('/image1.png', links)
        self.assertIn('/image2.png', links)
        self.assertIn('/script1.js', links)
        self.assertIn('/script2.js', links)
        self.assertIn('/favicon.ico', links)
        self.assertIn('/apple-touch-icon.png', links)
        self.assertIn('/apple-touch-icon.png', links)
        self.assertIn('/file1.html', links)
        self.assertIn('/file2.html', links)
        self.assertIn('/background.png', links)
        self.assertIn('/inline-js-file.html', links)

    def test_get_absolute_urls(self):
        links = list(self.parser.get_absolute_urls())
        self.assertEqual(len(links), 11)
        self.assertIn('http://www.example.com/image1.png', links)

    def test_get_actions(self):
        actions = self.parser.get_actions()
        actions = list(actions)
        self.assertEqual(len(actions), 3)


class TestCsslParser(unittest.TestCase):

    def setUp(self):
        self.parser = CssParser(css_sample, 'http://www.example.com')

    def tearDown(self):
        pass

    def test_get_urls(self):
        links = list(self.parser.get_urls())
        self.assertEqual(len(links), 7)
        self.assertIn('/img/file1.png', links)
        self.assertIn('/img/file2.png', links)
        self.assertIn('/img/file3.png', links)
        self.assertIn('/img/file4.png', links)
        self.assertIn('/img/file5.png', links)
        self.assertIn('/img/file6.png', links)
        self.assertIn('/img/file7.png', links)

    def test_get_imports(self):
        links = list(self.parser.get_imports())
        self.assertEqual(len(links), 6)
        self.assertIn('/css/file1.css', links)
        self.assertIn('/css/file2.css', links)
        self.assertIn('/css/file3.css', links)
        self.assertIn('/css/file4.css', links)
        self.assertIn('/css/file5.css', links)
        self.assertIn('/css/file6.css', links)

    def test_get_ressources(self):
        links = list(self.parser.get_ressources())
        self.assertEqual(len(links), 13)
        self.assertIn('/img/file1.png', links)
        self.assertIn('/img/file2.png', links)
        self.assertIn('/img/file3.png', links)
        self.assertIn('/img/file4.png', links)
        self.assertIn('/img/file5.png', links)
        self.assertIn('/img/file6.png', links)
        self.assertIn('/img/file7.png', links)
        self.assertIn('/css/file1.css', links)
        self.assertIn('/css/file2.css', links)
        self.assertIn('/css/file3.css', links)
        self.assertIn('/css/file4.css', links)
        self.assertIn('/css/file5.css', links)
        self.assertIn('/css/file6.css', links)

    def test_get_absolute_urls(self):
        links = list(self.parser.get_absolute_urls())
        self.assertEqual(len(links), 13)
        self.assertIn('http://www.example.com/img/file1.png', links)


class TestJavscriptParser(unittest.TestCase):

    def setUp(self):
        self.parser = JavascriptParser(js_sample, 'http://www.example.com')

    def tearDown(self):
        pass

    def test_get_string_urls(self):
        links = list(self.parser.get_string_urls())
        self.assertEqual(len(links), 2)
        self.assertIn('/directory/file1.html', links)
        self.assertIn('/directory/file2.html', links)

    def test_get_full_urls(self):
        links = list(self.parser.get_full_urls())
        self.assertEqual(len(links), 7)
        self.assertIn('http://foo.com/blah_blah', links)
        self.assertIn('http://foo.com/blah_blah/', links)
        self.assertIn('http://www.extinguishedscholar.com/wpglob/?p=364', links)
        self.assertIn('http://\xe2\x9c\xaadf.ws/1234', links)
        self.assertIn('http://\xe2\x9e\xa1.ws/\xe4\xa8\xb9', links)
        self.assertIn('http://example.com/something?with,commas,in,url', links)
        self.assertIn('http://WWW.EXAMPLE.COM', links)

    def test_get_mailto(self):
        links = list(self.parser.get_mailto())
        self.assertEqual(len(links), 2)
        self.assertIn('mailto:gruber@daringfireball.net?subject=TEST', links)
        self.assertIn('mailto:name@example.com', links)

    def test_get_ressources(self):
        links = list(self.parser.get_ressources())
        self.assertEqual(len(links), 11)
        self.assertIn('/directory/file1.html', links)
        self.assertIn('/directory/file2.html', links)
        self.assertIn('http://foo.com/blah_blah', links)
        self.assertIn('http://foo.com/blah_blah/', links)
        self.assertIn('http://www.extinguishedscholar.com/wpglob/?p=364', links)
        self.assertIn('http://\xe2\x9c\xaadf.ws/1234', links)
        self.assertIn('http://\xe2\x9e\xa1.ws/\xe4\xa8\xb9', links)
        self.assertIn('http://example.com/something?with,commas,in,url', links)
        self.assertIn('http://WWW.EXAMPLE.COM', links)
        self.assertIn('mailto:gruber@daringfireball.net?subject=TEST', links)
        self.assertIn('mailto:name@example.com', links)

    def test_get_absolute_urls(self):
        links = list(self.parser.get_absolute_urls())
        self.assertEqual(len(links), 11)
        self.assertIn('http://www.example.com/directory/file1.html', links)
