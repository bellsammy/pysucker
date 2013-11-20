# -*- coding: utf-8 -*-
import importlib
import os
from urlparse import urlparse

from celery import chain
import redis

from tasks import crawl, parse, robot, count


if os.environ.get("PYSUCKER_CONFIG_MODULE", None):
    conf = importlib.import_module(os.environ.get['PYSUCKER_CONFIG_MODULE'])
else:
    conf = importlib.import_module('pysucker.default_config')

r = redis.StrictRedis(host=conf.REDIS_HOST, port=conf.REDIS_PORT,
                      db=conf.REDIS_DB)

crawled_set = '{}_crawled'.format(conf.PS_PROJECT_NAME)
done_counter = '{}_done'.format(conf.PS_PROJECT_NAME)
allowed_hosts_set = '{}_allowed_host'.format(conf.PS_PROJECT_NAME)

r.set(done_counter, 0)

class Robot(object):
    """A web crawler and parser used to copy a website content to the locale
    file system.

    Args:
        base_urls (iter): URLs to start crawling.
        allowed_host (list): Allowed hosts to crawl.
    """
    
    def __init__(self, base_urls, allowed_hosts=None):
        """Set bases_urls and allowed hosts."""
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
        """Start crawling and parsing base_ressources if url not already
        crawled."""

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
        """Filter urls to remove not allowed host and already crawled urls.

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
        """Clean robot data sets from redis."""
        
        r.delete(crawled_set)
        r.delete(allowed_hosts_set)
        r.delete(done_counter)
        for k, v in conf.CELERY_ROUTES.iteritems():
            r.delete(v['queue'])
