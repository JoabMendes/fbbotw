
- Verify if your `~/.pypirc` file is set to:
```bash
[pypi]
username = <username>
password = <password>
```

-  Update the version on setup.py to the next release to be done.

-  Create the following env var

```bash
export SEED_VERSION_PREFIX=v
```

- Use the seed library to create the python package

```bash
# Subsequent releases can be done via ONE of:
seed release --bug    # A bug version pump (i.e. 0.0.1)
seed release --minor  # A minor version pump (i.e. 0.1.0)
seed release --major  # A major version pump (i.e. 1.0.0)
seed release          # Equivalent to seed release --bug
```

- Currently this library can't do the upload to the last version of pypi and
it will throw an error when after asking the pypi password.

- Use twine to run the upload:

```bash
twine upload dist/*
```
