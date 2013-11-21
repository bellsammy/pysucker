PySucker
========

**PySucker** is a Python web crawler used to copy a website content on the local file system for data extraction and modification.

It was originally developed and used to extract unstructured data from a large website.

Another usage was the creation of modified static copies (removing ads and broken links, updating tracking scripts, etc.) of old dynamic websites that are not updated anymore to reduce their hosting costs.

This project is an open-source rewrite of its main features.

Installation
------------

***WARNING*** This version is incomplete and not stable.

### Requirements

* Redis
* libxml

Note: PySucker was developed on Os X 10.7 and rewritten on Os X 10.9. It is run for production on Os X computers and Ubuntu servers. It was never tested on Windows.

### Unit testing

UnitTests can be run with [py.test](http://pytest.org/latest/) and [tox](http://tox.readthedocs.org/en/latest/).

```zsh
$ py.test --cov=pysucker --cov-report=html -n=4
```

Usage
-----

PySucker need [Celery](http://www.celeryproject.org) and [Redis](http://redis.io).

### Configuration

TODO.

### Start Redis

See [Redis documentation](http://redis.io/documentation).

PySucker use the default Redis configuration:

```
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
```

### Start Celery

To start a Celery worker with default address and value, run:

```zsh
$ celery worker -A pysucker.tasks -Q pysucker,pysucker_crawl,pysucker_parse --loglevel=warning
```

You should start multiple Celery workers to adjust concurrency with your application requirements. A basic usage on a 4 core machine with a 100Mb connexion:

```zsh
$ celery worker -A pysucker.tasks -Q pysucker -n pysucker_main --loglevel=warning
$ celery worker -A pysucker.tasks -Q pysucker_crawl -n pysucker_crawler --concurrency=4 --loglevel=warning
$ celery worker -A pysucker.tasks -Q pysucker_parse --concurrency=5 -n pysucker_parser --loglevel=warning
```

See [Celery documentation](http://docs.celeryproject.org/en/latest/index.html) for more options.

### Start PySucker from cli

#### Start

```zsh
$ python pysucker/command.py start -url http://httpstat.us -host httpstat.us
```

#### Stop and clean

To delete pending Celery tasks and Redis data, run:

```zsh
$ python pysucker/command.py clean
```

### Start PySucker from Python

#### Start

```Python
from pysucker.robot import Robot

robot = Robot('http://httpstat.us/', 'httpstat.us')
robot.start()
```

#### Stop and clean

```Python
from pysucker.robot import Robot

Robot.clean()
```