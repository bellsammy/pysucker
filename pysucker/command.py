#! /usr/bin/env python
"""PySucker CLI."""
import datetime
import time

from pysucker.robot import Robot, r, done_counter, crawled_set


def start(args):
    """Start a new Robot."""

    base_urls = args.url
    allowed_hosts = args.host
    robot = Robot(base_urls, allowed_hosts)
    robot.start()

    print '\033[94m'
    print 'Robot started.'
    print '\033[0m'

    try:
        logger()
    except KeyboardInterrupt:
        print '\033[91m'
        print 'WARNING: You need to call this script with `clean` command to \
stop and clean pending crawl'
        print '\033[0m'


def clean(args):
    """Clean Redis data."""

    Robot.clean()
    print '\033[94m'
    print 'Redis data cleaned.'
    print '\033[0m'


def logger():
    """Show crawl progress."""

    while True:
        message = 'Ressources: {}/{}'.format(r.get(done_counter),
                                             r.scard(crawled_set))
        print datetime.datetime.now(), message
        time.sleep(5)


def main():
    import argparse

    # Main parser
    epilog = 'See https://github.com/gvigneron/pysucker/'
    parser = argparse.ArgumentParser(prog='pysucker',
                                     description='CLI for PySucker crawler.',
                                     epilog=epilog)
    subparsers = parser.add_subparsers(title='subcommands',
                                       help='PySucker command to run')
    # Start command parser.
    parser_start = subparsers.add_parser('start', help='Start a new robot.')
    parser_start.add_argument('-url', type=str, nargs='+', required=True,
                              help='starting URL(s)')
    parser_start.add_argument('-host', type=str, nargs='+', required=True,
                              help='restrictive (list of) domain(s) to crawl')
    parser_start.add_argument('-conf', type=str, help='configuration module')
    parser_start.set_defaults(func=start)
    # Clean command parser.
    parser_clean = subparsers.add_parser('clean',
                                         help='Clean robot Redis data.')
    parser_clean.set_defaults(func=clean)

    args = parser.parse_args()
    args.func(args)
