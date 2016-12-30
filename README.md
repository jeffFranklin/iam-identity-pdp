[![Build Status](https://travis-ci.org/UWIT-IAM/iam-identity-pdp.svg?branch=master)](https://travis-ci.org/UWIT-IAM/iam-identity-pdp)
[![Coverage Status](https://coveralls.io/repos/github/UWIT-IAM/iam-identity-pdp/badge.svg?branch=master)](https://coveralls.io/github/UWIT-IAM/iam-identity-pdp?branch=master)

#Identity.UW Profile

##Development

The settings module is configured to run with mock data. settings.MOCK_LOGIN_USER
controls the user you want to be.

```bash
python manage.py runserver
```

##Running python tests


###From the command line
In your project directory

```bash
pip install tox
tox
```

###From within PyCharm
Add a new py.test configuration with the following settings...
```
Target: /home/you/projects/pdp/pdp
Options: --pep8
Environment variables: DJANGO_SETTINGS_MODULE=settings
Python interpreter: Your pdp virtualenv
Working directory: /home/you/projects/pdp
```

##Deploying
Example deploy to a docker instance...

```
cd ansible
./install.sh rivera_docker
```
