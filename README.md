# Swiss pairing game tournament

Tournament is a programn to generate game pairings using the Swiss pairing algorithm.

## Getting Started

Just clone the repository in your local machine

```
git clone https://github.com/rodbs/tournament.git
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

Start the database
```
sudo service potgresql start

```

Run the script to generate the database schema adn views
```
psql -f tournament.sql
```

Example to test it works:
```
python
import tournament
tournament.registerPlayer("Peter")
tournament.registerPlayer("John")
tournament.swissPairings()
tournament.playerStandings()
```

## Running the tests

Run this test:
```
python tournament_test.py
``` 

## Built With

* Clodu9


## Authors

* **Rodrigo Barriuso** - *Project for Udacity IPND* - [Udacity](https://github.com/udacity/fullstack-nanodegree-vm)

 