# -*- coding: utf-8 -*-
"""
Base parser that extract links from an HTML file.

Usage example:
    parser = Parser('/tmp/index.html.lz4')
    links = parser.get_ressources()
"""
import itertools
import json
import re
import urlparse

from bs4 import BeautifulSoup


class Parser(object):
    """Parser for link extraction from ressource.

    Extract file type from `<path>.meta` if exists, else assume file is html.

    Args:
        path (str): Lz4 compressed file path to parse.
    """

    _content = None

    def __new__(cls, path):
        content, meta = cls.load(path)
        content_type = meta.get('content-type', '').split(';')[0]
        if 'text/html' in content_type:
            return HtmlParser(content, meta.get('url', ''))
        elif 'text/css' in content_type:
            return CssParser(content, meta.get('url', ''))
        elif 'text/javascript' in content_type:
            return JavascriptParser(content, meta.get('url', ''))
        return super(Parser, cls).__new__(cls)

    @classmethod
    def load(cls, path):
        """Load file content and set metas.

        Args:
            path (str): Lz4 compressed file path to load.

        Returns:
            (tuple): (content, meta dict)
        """

        # Set defaults
        content = ''
        meta = {}
        # Set metas.
        try:
            with open(u'{}.meta'.format(path), 'r') as f:
                meta = json.loads(f.read())
        except IOError:
            pass
        # Load content
        try:
            with open(u'{}.data'.format(path), 'r') as f:
                content = f.read()
        except IOError:
            pass
        # Return
        return content, meta

    def get_ressources(self):
        """Extract relative URLs find in file.

        Returns:
            (iter): URLs.
        """

        return ()

    def get_absolute_urls(self):
        """Extract all ressources absolute urls from self.soup

        Returns:
            (iter): Absolute URLs.
        """

        return ()


class HtmlParser(object):
    """HTML parsing tools.

    Args:
        html_code (str): HTML to parse.
        source (str): Web ressource absolute URL.
    """

    def __init__(self, html_code, source=''):
        self.source = source
        self.soup = BeautifulSoup(html_code, "lxml", from_encoding='utf8')

    def get_ressources(self):
        """Extract all ressources urls from self.soup

        Returns:
            (iter): URLs.
        """

        links = self.get_links()
        scripts = self.get_scripts()
        imgs = self.get_images()
        css = self.parse_inline_css()
        js = self.parse_inline_scripts()
        return itertools.chain(links, scripts, imgs, css, js)

    def get_absolute_urls(self):
        """Extract all ressources absolute urls from self.soup

        Returns:
            (iter): Absolute URLs.
        """
        return (urlparse.urljoin(self.source, url) for url in self.get_ressources())

    def get_links(self):
        """Get all href from <link> and <a> tags.

        Returns:
            (iter): URLs.
        """

        a_href = (link.get('href').strip() for link in self.soup.find_all('a')
                  if link.get('href'))
        link_href = (link.get('href').strip() for link in
                     self.soup.find_all('link') if link.get('href'))
        return itertools.chain(a_href, link_href)

    def get_scripts(self):
        """Get all src from <scripts> tags.

        Returns:
            (iter): URLs.
        """

        return (script.get('src').strip() for script
                in self.soup.find_all('script') if script.get('src'))

    def get_images(self):
        """Get all src from <img> tags.

        Returns:
            (iter): URLs.
        """

        return (img.get('src').strip() for img in self.soup.find_all('img') if img.get('src'))

    def parse_inline_css(self):
        """Extract inline css and return ressources.

        Returns:
            (iter): URLs.
        """

        inlines = self.soup.find_all('style')
        for inline in inlines:
            if inline.string:
                for link in CssParser(inline.string).get_ressources():
                    yield link

    def parse_inline_scripts(self):
        """Extract inline javascripts and return ressources.

        Returns:
            (iter): URLs.
        """

        inlines = self.soup.find_all('script')
        for inline in inlines:
            if inline.string:
                for link in JavascriptParser(inline.string).get_ressources():
                    yield link

    def get_actions(self):
        """Extract forms action url.

        Returns:
            (iter): URLs.
        """

        return (form.get('action').strip() for form in self.soup.find_all('form'))


class CssParser(object):
    """CSS parsing tools.

    Args:
        css_code (str): HTML to parse.
        source (str): Web ressource absolute URL.
    """

    imports = r"""@import[\s\t]*["'](?P<url>.*)["'][\s\t]*;"""
    imports_re = re.compile(imports)

    urls = r"""url\([\s\t]*["']{0,1}(?P<url>[^"'();{}]*)["']{0,1}[\s\t]*\)"""
    urls_re = re.compile(urls)

    def __init__(self, css_code, source=''):
        self.source = source
        self.css_code = css_code

    def get_ressources(self):
        """Extract ressources urls form self.css_code

        Returns:
            (iter): URLs.
        """

        imports = self.get_imports()
        urls = self.get_urls()
        return itertools.chain(imports, urls)

    def get_absolute_urls(self):
        """Extract all ressources absolute urls from self.soup

        Returns:
            (iter): Absolute URLs.
        """
        return (urlparse.urljoin(self.source, url) for url in self.get_ressources())

    def get_imports(self):
        """Extract url from @import statement.

        Returns:
            (iter): URLs.
        """

        return (link.strip() for link in self.imports_re.findall(self.css_code))

    def get_urls(self):
        """Extract url from url() value.

        Returns:
            (iter): URLs.
        """

        return (link.strip() for link in self.urls_re.findall(self.css_code))


class JavascriptParser(object):
    """Javascript parsing tools.

    Args:
        js_code (str): HTML to parse.
        source (str): Web ressource absolute URL.
    """

    urls = r"""["'](?P<url>[a-zA-Z][\w-]+:/{1,3}[^\s()<>'"]+[.][a-zA-Z]{2,4}[^\s()<>"']+)["']"""
    urls_re = re.compile(urls)

    strings = r"""["'](?P<url>/[^\s()<>"']+\.[^\s()<>"';]{2,6})["']"""
    strings_re = re.compile(strings)

    mailto = r"""["'](?P<url>mailto\:[^\s()<>"']+)["']"""
    mailto_re = re.compile(mailto)

    def __init__(self, js_code, source=''):
        self.source = source
        self.js_code = js_code

    def get_ressources(self):
        """Extract ressources urls form self.js_code

        Returns:
            (iter): URLs.
        """

        urls = self.get_full_urls()
        strings = self.get_string_urls()
        mailtos = self.get_mailto()
        return itertools.chain(urls, strings, mailtos)

    def get_absolute_urls(self):
        """Extract all ressources absolute urls from self.soup

        Returns:
            (iter): Absolute URLs.
        """
        return (urlparse.urljoin(self.source, url) for url in self.get_ressources())

    def get_full_urls(self):
        """Extract full urls from self.js_code.

        Returns:
            (iter): URLs.
        """

        return self.urls_re.findall(self.js_code)

    def get_string_urls(self):
        """Extract urls set in strings variables.

        Returns:
            (iter): URLs.
        """

        return self.strings_re.findall(self.js_code)

    def get_mailto(self):
        """Extract mailto urls in self.js_code.

        Returns:
            (iter): URLs.
        """
        
        return self.mailto_re.findall(self.js_code)