# -*- coding: utf-8 -*-
import importlib
import os
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from celery import chain
import redis

from tasks import crawl, parse, robot, count


# Configuration.
conf_module = os.environ.get("PYSUCKER_CONFIG_MODULE", 'pysucker.default_config')
conf = importlib.import_module('pysucker.default_config')


# List of already find/crawled URLs.
crawled_set = '{}_crawled'.format(conf.PS_PROJECT_NAME)
# Counter of URLs already analyzed.
done_counter = '{}_done'.format(conf.PS_PROJECT_NAME)
# List of allowed host.
allowed_hosts_set = '{}_allowed_host'.format(conf.PS_PROJECT_NAME)


r = redis.StrictRedis(host=conf.REDIS_HOST, port=conf.REDIS_PORT,
                      db=conf.REDIS_DB)
r.set(done_counter, 0)


class Robot(object):
    """A web crawler to fetch web ressources, parses them to extract links, and
    analyzes them to extract data.

    Args:
        base_urls (iter): URLs to start crawling.
        allowed_host (list): Allowed hosts to crawl.
    """
    
    def __init__(self, base_urls, allowed_hosts=None):
        """Set `self.bases_urls` and `self.allowed_hosts`."""

        self.base_urls = base_urls if hasattr(base_urls, '__iter__') \
                         else [base_urls]
        # Set allowed hosts
        if allowed_hosts is None:
            self.allowed_hosts = list(r.smembers(allowed_hosts_set))
        else:
            self.allowed_hosts = list(allowed_hosts) \
                                 if hasattr(allowed_hosts, '__iter__') \
                                 else [allowed_hosts]
            r.sadd(allowed_hosts_set, *self.allowed_hosts)

    def start(self):
        """Start crawling and parsing filtered `base_urls`.
        """

        # Filter urls.
        urls = self.filter_urls(self.base_urls)
        
        for url in urls:
            # Call tasks.
            res = chain(crawl.s(url, conf.RESSOURCES_PATH),
                        parse.s(),
                        robot.s(),
                        count.s())()
            # Mark as crawled.
            r.sadd(crawled_set, url)

    @classmethod
    def filter_urls(cls, urls):
        """Filter `urls` to remove not allowed hosts and already crawled urls.

        Args:
            urls (iter): URLs to filter.

        Returns:
            (iter): Filtered URLs.
        """

        urls = (url for url in urls if not r.sismember(crawled_set, url))
        urls = (url for url in urls
                if r.sismember(allowed_hosts_set, urlparse(url).netloc))
        return urls

    @classmethod
    def clean(cls):
        """Clean robot data in Redis."""
        
        r.delete(crawled_set)
        r.delete(allowed_hosts_set)
        r.delete(done_counter)
        for k, v in conf.CELERY_ROUTES.iteritems():
            r.delete(v['queue'])
