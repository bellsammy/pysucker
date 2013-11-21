# -*- coding: utf-8 -*-

PS_PROJECT_NAME = 'pysucker'

# Crawler and Parser.
from pysucker.parser import Parser
PS_PARSER = Parser

# Directory to save crawled ressources.
RESSOURCES_PATH = '/tmp/pysucker'

# Redis config.
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Celery config.
BROKER_URL = 'redis://{}:{}/{}'.format(REDIS_HOST, REDIS_PORT, REDIS_DB)
#CELERY_RESULT_BACKEND = 'redis://{}:{}/{}'.format(REDIS_HOST, REDIS_PORT, REDIS_DB)

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']

# CELERY TIMEZONE
CELERY_TIMEZONE = 'Europe/Paris'
CELERY_ENABLE_UTC = True

# CELERY ROUTES
CELERY_ROUTES = {'pysucker.tasks.crawl': {'queue': '{}_crawl'.format(PS_PROJECT_NAME)},
                 'pysucker.tasks.parse': {'queue': '{}_parse'.format(PS_PROJECT_NAME)},
                 'pysucker.tasks.robot': {'queue': PS_PROJECT_NAME},
                 'pysucker.tasks.count': {'queue': PS_PROJECT_NAME},}