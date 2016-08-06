#!/usr/bin/python
import argparse
import os
import requests

parser = argparse.ArgumentParser()
parser.add_argument(
    "--repository",
    action="store", help="is there a repository there",
    required=True,
)
parser.add_argument(
    "--package", 
    action="store", help="name of package",
    required=True,
)
parser.add_argument(
    "--version",
    action="store", help="version of package",
    required=True,
)
args = parser.parse_args()

repository = args.repository
package = args.package
version = args.version

if not os.path.isdir(repository):
    raise Exception(
        "I cannot find the repository {0} in the directory {1}.".format(
            repository, os.getcwd()
        )
    )

pypi_base_url = 'https://pypi.python.org/simple'
package_url = "{0}/{1}".format(pypi_base_url, package)

r = requests.get(package_url)
if r.status_code != 200:
    raise Exception(
        "There is nothing at the URL {0}. Does the package {1} exist?".format(
            package_url, package
        )
    )

