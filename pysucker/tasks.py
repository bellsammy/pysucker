# -*- coding: utf-8 -*-
"""Celery tasks."""
import httplib
import importlib
import os

from celery import Celery
from celery.utils.log import get_task_logger

from pysucker.crawler import Crawler
from pysucker import __version__


# Configuration.
conf_module = os.environ.get("PYSUCKER_CONFIG_MODULE", 'pysucker.default_config')
conf = importlib.import_module('pysucker.default_config')

app = Celery('pysucker')
app.config_from_object(conf_module)
logger = get_task_logger(__name__)

# Load Parser
Parser = conf.PS_PARSER


@app.task(name='pysucker.tasks.crawl', bind=True)  # rate_limit='4/s'
def crawl(self, absolute_url, ressources_dir,
          user_agent='PySucker {}'.format(__version__),
          language='en-US'):
    """Run a new Crawler to fetch the given url.

    Args:
        absolute_url (str): URL to fetch.
        ressources_dir (str): Base path to save file.
        user_agent (str): Crawler user-agent.
        language (str): HTTP header 'Accept-Language'.

    Returns:
        (str): File path with ressource.
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
    """Run a new parser to extract links from the given file.

    Args:
        path (str): File path to parse.

    Returns:
        (list): URLs to parse, extracted from file.
    """

    parser = Parser(path)
    urls = parser.get_absolute_urls()
    return list(urls)


@app.task(name="pysucker.tasks.robot")
def robot(base_urls):
    """Run a new robot for the given urls.

    Args:
        base_urls (iter): URLs to start crawling.
    """

    from robot import Robot

    robot = Robot(base_urls)
    robot.start()


@app.task(name='pysucker.tasks.count')
def count(*args):
    """Increment counter of URLs already analyzed."""

    from robot import r, done_counter

    r.incr(done_counter)
