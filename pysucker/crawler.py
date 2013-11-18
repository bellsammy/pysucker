# -*- coding: utf-8 -*-
"""
A simple crawler to fetch and save http ressources.

Ressource are compressed with lz4.

Usage example:
    url = 'http://www.example.com'
    crawler = Crawler(url, '/tmp/ressources')
    if crawler.fetch():
        crawler.save()
"""
import httplib
import os
import urllib
import urlparse

import lz4

from pysucker import __version__


class Crawler(object):
    """A simple crawler to fetch and save http ressources.

    Args:
        absolute_url (str): URL to fetch.
        ressources_dir (str): Base path to save file.
        file_name (str): File name to save ressource.
        user_agent (str): Crawler user-agent.
        language (str): HTTP header 'Accept-Language'.
    """
    
    def __init__(self, absolute_url, ressources_dir, file_name=None,
                 user_agent='PySucker {}'.format(__version__),
                 language='en-US'):
        super(Crawler, self).__init__()
        self.absolute_url = absolute_url
        self.ressources_dir = ressources_dir
        if file_name:
            self.file_name = file_name
        else:
            self.url_to_filename()
        self.request_headers = {'User-Agent': user_agent,
                                'Accept-Language': language}

    def url_to_filename(self, default='index.html'):
        """Extract path and filename from url.

        Args:
            default (str): Default filename.
        """

        url = urlparse.urlparse(self.absolute_url)
        # Set file name.
        base_name = os.path.basename(url.path)
        filename = base_name if base_name else default
        if url.query:
            filename = u'{}?{}'.format(filename, url.query)
        self.file_name = filename
        # Update path.
        dir_name = os.path.dirname(url.path)
        if dir_name and dir_name is not '/':
            self.ressources_dir = '{}{}'.format(self.ressources_dir, dir_name)

    def fetch(self):
        """Fetch url_to_crawl, extract response header and content.

        Returns:
            bool -- True if ok, False if error
        """
        url = urlparse.urlparse(self.absolute_url)
        connexion = httplib.HTTPConnection(url.netloc)
        request_url = u'{0}?{1}'.format(url.path, url.query) if url.query \
                      else urllib.quote(url.path.encode('utf8'))
        # Fetch
        connexion.request("GET", request_url, headers=self.request_headers)
        self.response = connexion.getresponse()
        if self.response.status == 200:
            return True
        else:
            return False

    def save(self):
        """Compress and save response content if http status code is 200."""

        if self.response.status == 200:
            # Check if directory exist.
            if not os.path.exists(self.ressources_dir):
                os.makedirs(self.ressources_dir)
            # Save compressed data.
            path = '{}/{}.lz4'.format(self.ressources_dir, self.file_name)
            with open(path, 'w') as f:
                compressed_data = lz4.dumps(self.response.read())
                f.write(compressed_data)
