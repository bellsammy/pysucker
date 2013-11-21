#! /usr/bin/env python
import datetime
import time

from robot import Robot, r, done_counter, crawled_set


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
        print 'WARNING: You need to call this script with `clean` command to stop and clean pending crawl'
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
        print datetime.datetime.now(), 'Ressources: {}/{}'.format(r.get(done_counter) ,r.scard(crawled_set))
        time.sleep(5)


if __name__ == "__main__":
    import argparse

    # Main parser
    parser = argparse.ArgumentParser(prog='pysucker',
        description='CLI for PySucker crawler.',
        epilog='See https://github.com/gvigneron/pysucker/')
    subparsers = parser.add_subparsers(title='subcommands',
        help='PySucker command to run')
    # Start command parser.
    parser_start = subparsers.add_parser('start', help='Start a new robot.')
    parser_start.add_argument('-url',
        type=str,
        nargs='+',
        required=True,
        help='starting URL(s)')
    parser_start.add_argument('-host',
        type=str,
        nargs='+',
        required=True,
        help='restrictive (list of) domain(s) to crawl')
    parser_start.add_argument('-conf',
        type=str,
        help='configuration module')
    parser_start.set_defaults(func=start)
    # Clean command parser.
    parser_clean = subparsers.add_parser('clean', help='Clean robot Redis data.')
    parser_clean.set_defaults(func=clean)

    args = parser.parse_args()
    args.func(args)