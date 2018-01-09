import os
import shutil
import subprocess as sp
import sys

from setuptools import find_packages, setup


def remove_build_files():
    for f in ('build', 'dist', 'sqlwriter.egg-info'):
        if os.path.exists(f):
            shutil.rmtree(f)


def do_setup():
    remove_build_files()

    setup(
        name='sqlwriter',
        description="Writes pandas DataFrame to several flavors of sql database",
        license="MIT",
        version='1.0.1',
        packages=find_packages(),
        include_package_data =True,
        install_requires=['pandas==0.21.0'],
        author='',
        author_email='',
        url='',
        scripts=['sqlwriter/bin/sqlwriter'],
    )


if __name__ == '__main__':
    do_setup()
