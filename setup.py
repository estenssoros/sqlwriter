import subprocess as sp
import sys

from setuptools import setup


def check():
    """Check the source code to make sure there are no syntax failures"""
    cmd = "python -m pyflakes ."
    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE)
    p.wait()
    out, err = p.communicate()
    if out:
        print('PYFLAKES:')
        print(out)
        sys.exit(1)


def do_setup():
    check()
    setup(
        name='sqlwriter',
        description="Writes pandas DataFrame to several flavors of sql database",
        license="MIT License",
        version='1.0.0',
        packages=['sqlwriter', ],
        install_requires=[
            'pandas==0.20.3',
            'tqdm==4.19.1',
            'pymssql==2.1.3',
            # 'cx-Oracle==6.0.2',
            'psycopg2==2.7.3.1',
        ]
    )


if __name__ == '__main__':
    do_setup()
