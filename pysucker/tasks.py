# -*- coding: utf-8 -*-
"""Celery tasks."""
import httplib
import os

from celery import Celery
from celery.utils.log import get_task_logger

from crawler import Crawler
from parser import Parser
from pysucker import __version__


app = Celery('pysucker')
if os.environ.get("PYSUCKER_CONFIG_MODULE", None):
    app.config_from_envvar("PYSUCKER_CONFIG_MODULE")
else:
    app.config_from_object('pysucker.default_config')
logger = get_task_logger(__name__)


@app.task(name='pysucker.tasks.crawl') # rate_limit='4/s'
def crawl(absolute_url, ressources_dir,
          user_agent='PySucker {}'.format(__version__),
          language='en-US'):
    """Run a new Crawler for the given url.

    Args:
        absolute_url (str): URL to fetch.
        ressources_dir (str): Base path to save file.
        user_agent (str): Crawler user-agent.
        language (str): HTTP header 'Accept-Language'.

    Returns:
        (str): File with ressource path.
    """

    crawler = Crawler(absolute_url, ressources_dir,
                      user_agent='PySucker {}'.format(__version__),
                      language='en-US')
    if crawler.fetch():
        crawler.save()
    elif crawler.response is None:
        logger.error('httplib.HTTPException at {}'.format(absolute_url))
        raise self.retry(exc=httplib.HTTPException())
    else:
        logger.error('HTTP error {} at {}'.format(crawler.response.status,
                                                 absolute_url))
        crawler.save()
        raise self.retry(exc=ValueError())
    return crawler.file_path()


@app.task(name='pysucker.tasks.parse')
def parse(path):
    """Run a new parser for the given file.

    Args:
        path (str): Lz4 compressed file path to parse.

    Returns:
        (list): URLs to parse, extracted from file.
    """

    parser = Parser(path)
    urls = parser.get_absolute_urls()
    return list(urls)


@app.task(name="pysucker.tasks.robot")
def robot(base_urls):
    """Ruen a new robot for the given urls.

    Args:
        base_urls (iter): URLs to start crawling.
    """

    from robot import Robot

    robot = Robot(base_urls)
    robot.start()


@app.task(name='pysucker.tasks.count')
def count(*args):
    """Increment done counter."""

    from robot import r, done_counter

    r.incr(done_counter)
