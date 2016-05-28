# Project Comport

[![Build Status](https://travis-ci.org/codeforamerica/comport.svg?branch=master)](https://travis-ci.org/codeforamerica/comport)

## What is it?

An ETL Toolkit to take Police Accountability data from the IA Pro Internal Affairs Software and produce publicly available and useful websites allowing better citizen oversight.

#### What's the status?
Project Comport is in early development.

## Who made it?
Project Comport is a project of the 2015 Indianapolis Code for America [fellowship team](http://codeforamerica.org/governments/indianapolis).

## How

#### Core Dependencies
Project Comport is a [Flask](http://flask.pocoo.org/) app. It uses [Postgres](http://www.postgresql.org/) for a database and uses [bower](http://bower.io/) to manage its front end dependencies. Big thanks to the [cookiecutter-flask](https://github.com/sloria/cookiecutter-flask) project for a nice kickstart.

#### Installation and setup

##### Quick local installation

First, clone the repo and change into the project directory.

```bash
git clone git@github.com:codeforamerica/comport.git
cd comport
```

Create a Python 3 virtual environment with [virtualenv](https://virtualenv.pypa.io/en/stable/) and (optionally) [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) and activate it. Read these [detailed installation and usage instructions](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for those two tools if you don't have them installed already.

With virtualenv only:

``` bash
virtualenv --no-site-packages -p python3 venv
source venv/bin/activate
```

With virtualenvwrapper:

``` bash
mkvirtualenv --no-site-packages -p python3 comport
workon comport
```

Then install the required packages:

```bash
pip install -r requirements/dev.txt
```

And create and populate the project database (use [postgres.app](http://postgresapp.com/) if you're developing on OS X):

```bash
psql -c 'create database comport;'
python manage.py db upgrade
```

[Bower](http://bower.io/) is used to install front-end dependencies. [Install node and npm](https://nodejs.org/), then use npm to [install bower](http://bower.io/#install-bower). When Bower's installed, use it to install Comport's front-end dependencies:

```bash
bower install
```

Finally, start the server:

```bash
python manage.py server
```

**NOTE**: The app's configuration lives in [`settings.py`](https://github.com/codeforamerica/comport/blob/master/comport/settings.py). When different configurations (such as `DevConfig`) are referenced in the next sections, they are contained in that file.

If you want to send a notification to a Slack instance on certain events, copy the `env.sample` file to `.env`:

```
cp env.sample .env
```

[Set up an Incoming Webhooks integration on Slack](https://my.slack.com/services/new/incoming-webhook) and save the value of **Webhook URL** as `SLACK_WEBHOOK_URL` in `.env`. This will not work when you're running Comport for development. To set the variable when the application is running on Heroku, [follow these instructions](https://devcenter.heroku.com/articles/config-vars).

#### Generating Fake Data

To generate some fake incident data, first start the server.

```bash
python manage.py server
```

Then, in another terminal, run the command below.

*WARNING: This command will destroy and re-build the application's database from scratch, erasing departments, users, incidents, etc.*

```bash
python manage.py test_client
```

#### Testing

In order to run the tests, you will need to create a test database. You can follow the same procedures outlined in the install section. By default, the database should be named `comport_test`:

```bash
psql
create database comport_test;
```

To run the tests, run

```bash
python manage.py test
```

from inside the root directory.

## License
See [LICENSE.md](https://github.com/codeforamerica/comport/blob/master/LICENSE.md).
