from setuptools import setup


def do_setup():
    setup(
        name='sqlwriter',
        description="Writes pandas DataFrame to several flavors of sql database",
        license="MIT License",
        version='1.0.0',
        packages=['sqlwriter',],
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
