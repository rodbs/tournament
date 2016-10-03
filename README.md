# Project Title

Tournament is a programn to generate game pairings using the Swiss pairing algorithm.

## Getting Started

Just clone the repository in your local machine

```
git clone 
```

### Prerequisities

You need Python 2.7 with the following libraries

```
sudo apt-get install python2.7
```

You also need PostgreSQL
```
sudo apt-get install postgresql-9.3
```

Install Python API for PostgreSQL:
```
sudo pip install psycopg2
```

### Installing

1. Start the database
```
sudo service potgresql start

```
2. Create user 'ubuntu' if it doesn't exit
```
psql 
create role ubutu with login password ubuntu
```

2. Run the script to generate the database schema
```
psql -f tournament.sql
```

3. Example to test it works:

 ```
python
import tournament
tournament.registerPlayer("Peter")
tournament.registerPlayer("John")
tournament.swissPairings()
tournament.playerStandings()
```

## Running the tests

Run the this test:
```
python tournamnet_test.py
``` 

## Built With

* Clodu9


## Authors

* **Rodrigo Barriuso** - *Project for Udacity IPND* - [Udacity](https://github.com/udacity/fullstack-nanodegree-vm)

 