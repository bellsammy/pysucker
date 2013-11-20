from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import codecs
import os
import sys
import re


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


long_description = """
"""

class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


setup(
    name='pysucker',
    version=find_version('pysucker', '__init__.py'),
    url='http://github.com/gvigneron/pysucker/',
    license='Apache Software License',
    author='Gregoire Vigneron',
    tests_require=['tox'],
    install_requires=['lz4>=0.6.0',
                      'redis>=2.8.0',
                      'hiredis>=0.1.1',
                      'celery>=3.1.4',
                      'beautifulsoup4>=4.3.2',
                      'lxml>=3.2.4'],
    cmdclass={'test': Tox},
    description='Web crawler and parser used to copy a website content to the locale file system.',
    long_description=long_description,
    packages=['pysucker'],
    include_package_data=True,
    platforms='any',
    test_suite='pysucker.test.test_pysucker',
    classifiers = [
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        ],
    extras_require={
        'testing': ['pytest'],
      }
)