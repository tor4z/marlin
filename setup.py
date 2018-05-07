import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


PACKAGE = "marlin"
NAME = PACKAGE
DESCRIPTION = "Python web crawler engine"
AUTHOR = "tor4z"
AUTHOR_EMAIL = "vwenjie@hotmail.com"
URL = "https://github.com/tor4z/marlin"
LICENSE = "MIT License"
VERSION = 0.1
TESTS_REQUIRE = ["pytest"]
CMDCLASS = {"test": PyTest}


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      url=URL,
      tests_require=TESTS_REQUIRE,
      cmdclass=CMDCLASS,
      packages=find_packages(exclude=["tests"]))
