#!/usr/bin/python
import argparse
import os
import requests
import shutil


def nprint(str):
    print("{0}\n".format(str))

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
parser.add_argument(
    "--rebuild",
    action="store_true", help="delete the package if it exists",
    default=False
)

args = parser.parse_args()

repository = args.repository
package = args.package
version = args.version
rebuild = args.rebuild

print("")

if rebuild:
    nprint(
        "Extracting package {0}, version {1}, into repository {2}, from scratch.".format(
            package, version, repository
        )
    )
else:
    nprint(
        "Extracting package {0}, version {1}, into repository {2}.".format(
            package, version, repository
        )
    )

if not os.path.isdir(repository):
    raise Exception(
        "I cannot find the repository {0} in the directory {1}.".format(
            repository, os.getcwd()
        )
    )

pypi_base_url = 'https://pypi.python.org'
pypi_simple_base_url = 'https://pypi.python.org/simple'
package_url = "{0}/{1}".format(pypi_simple_base_url, package)

nprint("Inspecting the URL {0}.".format(package_url))
r = requests.get(package_url)
if r.status_code != 200:
    raise Exception(
        "There is nothing at the URL {0}. Does the package {1} exist?".format(
            package_url, package
        )
    )

elements = r.text.split('\n')
expected_tgz_file = "{0}-{1}.tar.gz".format(package, version)

relevant_elements = [
    elt 
    for elt in elements 
    if expected_tgz_file in elt
]

if len(relevant_elements) == 0:
    raise Exception(
        "I cannot find a link to the specific file {0} on the page {1}.".format(
            expected_tgz_file, package_url
        )
    )

nprint("Found file {0} on the internet.".format(expected_tgz_file))

relative_link = relevant_elements[0].split("\"")[1]
absolute_link = "{0}/{1}".format(
    pypi_base_url,
    relative_link[len("../../"):]
)
nprint(absolute_link)

packages_dir = "{0}/{1}".format(repository, "packages")
if not os.path.isdir(packages_dir):
    os.mkdir(packages_dir)

specific_package_dir = "{0}/{1}".format(packages_dir, package)

if os.path.isdir(specific_package_dir):
    if rebuild == False:
        raise Exception(
            "You already have a {0} directory. Perhaps you meant to use '--rebuild'?".format(
                specific_package_dir
            )
        )
    else:
        nprint("Removing local directory {0}.".format(specific_package_dir))
        shutil.rmtree(specific_package_dir)

nprint("Creating local directory {0}.".format(specific_package_dir))
os.mkdir(specific_package_dir)






