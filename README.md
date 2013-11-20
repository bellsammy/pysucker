PySucker
========

Documentation
-------------

**PySucker** is a simple and flexible web crawler and parser used to copy a website content to the locale file system.

## Usage

PySucker use Celery with Redis as broker.

### Start Redis

### Start Celery

To start Celery with default address and value, run:
```zsh
$ celery worker -A pysucker.tasks -Q pysucker,pysucker_crawl,pysucker_parse --loglevel=error
```

You should start multiple Celery workers to adjust concurrency with your application requirements. A basic usage on a 4 core machine with a 100Mb connexion:
```zsh
celery worker -A pysucker.tasks -Q pysucker -n pysucker_main --loglevel=warning
celery worker -A pysucker.tasks -Q pysucker_crawl -n pysucker_crawler --concurrency=4 --loglevel=warning
celery worker -A pysucker.tasks -Q pysucker_parse --concurrency=5 -n pysucker_parser --loglevel=warning
```

### Start PySucker

## Requirements

* Redis
* libxml

## Unit testing

Tests can be run with [tox](http://tox.readthedocs.org/en/latest/) or [py.test](http://pytest.org/latest/):
```zsh
$ py.test --cov=pysucker --cov-report=html -n=4
```
