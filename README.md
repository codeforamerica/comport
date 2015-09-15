# comport


## Installation

1. Clone the repository and cd into it.
1. Create a database in PostgreSQL named `comport`
2. Run `make setup`. This installs both front end and back end libraries and adds tables to the database.

Recap

```bash
git clone https://github.com/codeforamerica/comport.git
cd comport
psql -c 'create database comport;'
make setup
```
