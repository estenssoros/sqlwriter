Database connectors:
====================
**mysql**

``
$ brew install mysql
``

**MySQLdb**

download from http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python

``
pip install mysqlclient-1.3.8-cp27-cp27m-win_amd64.whl
``


How to build and upload
-----------------------

$HOME/.pypirc:

.. code-block:: console

 [distutils]
 index-servers = pypi
 [pypi]
 repostitory = http://pypi.python.org/pypi
 username = <username>
 password = <password>

Then:

.. code-block:: pycon

 $ python setup.py sdist upload -r pypi

Testing
-------

We need multiple databases to test against: use docker compose

**Build Oracle Docker Container**

.. code-block:: pycon

 $ git clone https://github.com/oracle/docker-images.git
 $ cd docker-images/OracleDatabase/dockerfiles/12.2.0.1

visit `http://www.oracle.com/technetwork/database/enterprise-edition/downloads/index.html` and download `linuxx64_12201_database.zip` to the 12.2.0.1 directory

``
$ ./buildDockerImage.sh -v 12.2.0.1 -s
``

this will create the docker image `oracle/database:12.2.0.1-se2`


Bring up the stack:

``
$ docker-compose up --force-recreate --build
``

Run Tests...

Bring the stack down:

``
$ docker-compose down --volumes
``

debug a container:

.. code-block:: console

 $ docker ps -a
 $ docker exec -it <container name> bash


delete all images and containers:

.. code-block:: console

 $ docker rm $(docker ps -a -q)
 $ docker rmi $(docker images -q)
