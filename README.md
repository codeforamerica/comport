# Project Comport

## What is it?

An ETL Toolkit to take Police Accountability data from the IA Pro Internal Affairs Software and produce publicly available and useful websites allowing better citizen oversight.

#### What's the status?
Project Comport is in early development.

## Who made it?
Project Comport is a project of the 2015 Inidanapolis Code for America [fellowship team](http://codeforamerica.org/governments/indianapolis).

## How

#### Core Dependencies
Project Comport is a [Flask](http://flask.pocoo.org/) app. It uses [Postgres](http://www.postgresql.org/) for a database and uses [bower](http://bower.io/) to manage most of its front end dependencies. Big thanks to the [cookiecutter-flask](https://github.com/sloria/cookiecutter-flask) project for a nice kickstart.

It is highly recommended that you use use [virtualenv](https://readthedocs.org/projects/virtualenv/) (and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) for convenience). For a how-to on getting set up, please consult this [howto](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md). Additionally, you'll need node to install bower (see this [howto](https://github.com/codeforamerica/howto/blob/master/Node.js.md) for more on Node), and it is recommended that you use [postgres.app](http://postgresapp.com/) to handle your Postgres (assuming you are developing on OSX).

#### Installation and setup

##### Quick local installation using Make

First, create a python 3 virtualenv and activate it. Then:

```bash
git clone git@github.com:codeforamerica/comport.git
# create the 'comport' database
psql -c 'create database comport;'
python manage.py db upgrade
python manage.py load_test_data
python manage.py server
```


**NOTE**: The app's configuration lives in [`settings.py`](https://github.com/codeforamerica/comport/blob/master/comport/settings.py). When different configurations (such as `DevConfig`) are referenced in the next sections, they are contained in that file.

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
