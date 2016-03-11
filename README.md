[![Build Status](https://travis-ci.org/UWIT-IAM/iam-identity-pdp.svg?branch=master)](https://travis-ci.org/UWIT-IAM/iam-identity-pdp)
[![Coverage Status](https://coveralls.io/repos/github/UWIT-IAM/iam-identity-pdp/badge.svg?branch=master)](https://coveralls.io/github/UWIT-IAM/iam-identity-pdp?branch=master)

Personal Data Preferences
-------------------------

Essential information about this project to go here...

Development
-----------

pdp-site/settings.py is configured to run with mock data. Currently
only javerage works.  To run as javerage you can declare REMOTE_USER
at startup such as the following:

```bash
REMOTE_USER=javerage python manage.py runserver
```

Setup with PyCharm
------------------

###Setting up py.test###

See [here](https://wiki.cac.washington.edu/x/MqUnB)



Running python tests
--------------------

To run tests in your local environment do the following from this
directory

```bash
pip install tox
tox
```

The first run might take a minute to load dependencies but you should
be set after that.
