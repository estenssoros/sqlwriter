# sqlwriter

Writes pandas DataFrame to several flavors of sql database

### Flavors

- Postres
- Microsoft SQL
- MySQL
- Oracle

## Database connectors:
### mysql

```
$ brew install mysql
```


## How to build and upload

$HOME/.pypirc

```
[distutils]
index-servers = pypi
[pypi]
repostitory = http://pypi.python.org/pypi
username = <username>
password = <password>
```
Then:
```
$ python setup.py bdist
$ python setup.py bdist_wheel
$ twine upload dist/*
```
## Testing

We need multiple databases to test against-- docker compose

Bring up the stack:

```
$ docker-compose up --force-recreate --build
```

Run Tests...

Bring the stack down:

```
$ docker-compose down --volumes
```

debug a container:

```
$ docker ps -a
$ docker exec -it <container name> bash
```
delete all images and containers:
```
$ docker rm $(docker ps -a -q)
$ docker rmi $(docker images -q)
```
