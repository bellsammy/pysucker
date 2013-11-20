# -*- coding: utf-8 -*-
"""
A simple crawler to fetch and save http ressources.

Usage example:
    url = 'http://www.example.com'
    crawler = Crawler(url, '/tmp/ressources')
    if crawler.fetch():
        crawler.save()
"""
import httplib
import json
import os
import socket
import urllib
import urlparse

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
    
    def __init__(self, absolute_url, ressources_dir,
                 user_agent='PySucker {}'.format(__version__),
                 language='en-US'):
        super(Crawler, self).__init__()
        self.absolute_url = absolute_url
        self.ressources_dir = ressources_dir
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
        dir_name = os.path.dirname(url.path).rstrip('/')
        self.ressources_dir = '{}/{}{}'.format(self.ressources_dir, url.netloc,
                                               dir_name)

    def fetch(self):
        """Fetch url_to_crawl and extract response.

        Returns:
            (bool): True if ok, False if error
        """

        url = urlparse.urlparse(self.absolute_url)
        connexion = httplib.HTTPConnection(url.netloc)
        request_url = u'{0}?{1}'.format(url.path, url.query) if url.query \
                      else urllib.quote(url.path.encode('utf8'))
        # Fetch
        try:
            connexion.request("GET", request_url, headers=self.request_headers)
            self.response = connexion.getresponse()
        except (httplib.HTTPException, socket.gaierror), e:
            self.response = None
            return False
        if self.response.status < 500:
            return True
        else:
            return False
        
    def file_path(self):
        """Returns file path."""

        return u'{}/{}'.format(self.ressources_dir, self.file_name)

    def ensure_directory(self):
        """Create ressource directory if not already exist."""

        if not os.path.exists(self.ressources_dir):
            os.makedirs(self.ressources_dir)

    def save(self):
        """Save response meta data. Save response content.

        Text content is compressed with lz4.
        """

        # Check if directory exist.
        self.ensure_directory()
        # Save meta
        with open(u'{}.meta'.format(self.file_path()), 'w') as f:
            origin = dict(self.response.getheaders())
            meta = {'url': self.absolute_url,
                    'content-type': origin.get('content-type', ''),
                    'status': self.response.status}
            if origin.get('location', None):
                meta['location'] = origin['location']
            json.dump(meta, f)
        # Save compressed data.
        with open(u'{}.data'.format(self.file_path()), 'w') as f:
            f.write(self.response.read())
