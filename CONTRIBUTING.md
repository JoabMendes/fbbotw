# Contributing to FBBOTW

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to fbbotw, which is hosted on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document and to the package in a pull request.

## Installing

### 1 Clone the repository
```sh
$ git clone https://github.com/JoabMendes/fbbotw
```

### 2 After cloning, create your virtual environment (This example uses [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/)):

```sh
# Using virtualenvwrapper (pip install virtualenvwrapper)
$ mkvirtualenv -p `which python3` fbbotw #Keep the name as fbbotw, some script depend on this
```

### 3 Working on the environment, install de dependencies:

```sh
$ pip install -r requirements_dev.txt
```

### 4 Run the `setvars.sh` script to set some env var for testing.

```
$ ./setvars.sh
# Restart the env
$ deactivate
$ workon fbbotw
```

### 5 Do your changes :sparkle: 
![Uncle Ben is watching you](https://mafrinha.files.wordpress.com/2015/02/with-great-power-comes-great-responsibility.png)

- This package uses pep8, pyflakes and co for styling. And flake8 package for style check on tests.
- [Go pythonic](https://blog.startifact.com/posts/older/what-is-pythonic.html)

### 6 Run the tests

```sh
# will test functions and pep8 style with flake8
$ ./test.sh
```
### Create your pull request

Please use this template for your pull request:

```
## Requirements (List of requirement updates)
    - Filling out the template is required. Any pull request that does not include enough information to be reviewed in a timely manner may be closed at the maintainers' discretion.
    - All new code requires tests to ensure against regressions
## Description of the Change
## Alternate Designs
## Why Should This Be In Core? (Justify your changes)
## Benefits (Why will this make the package better)
## Possible Drawbacks
## Applicable Issues
```

### Documentation

- Add the necessary documentation to your code and the reference for the [facebook docs](https://developers.facebook.com/docs/messenger-platform/) if needed.

