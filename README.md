# sqlwriter

Writes pandas DataFrame to several flavors of sql database

### Flavors

- Postres

- Microsoft SQL

- MYSQL

- Oracle


# TODO

- everything


## how to build and upload

create $HOME/.pypirc

```
[distutils]
index-servers = pypi
[pypi]
repostitory = http://pypi.python.org/pypi
username = <username>
password = <password>
```

$ python setup.py bdist
$ python setup.py bdist_wheel
$ twine upload dist/*
