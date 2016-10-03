#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

from collections import Counter
import random
import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("delete  from matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("delete  from players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("select count(id) from players")
    rows = cur.fetchone()
    return int(rows[0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    sql = "INSERT INTO players (name) VALUES (%s);"
    data = (name,)
    cur.execute(sql, data)
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()

    players = {}
    cur.execute("select id , name from players ;")
    players_rows = cur.fetchall()
    for i in players_rows:
        players[i[0]] = i[1]

    cur.execute("select winner as id , count(winner) as matches  from matches group by winner;")
    wins_rows = cur.fetchall()
    wins = {}
    losses = {}
    matches = {}
    for i in wins_rows:
        wins[i[0]] = int(i[1])

    cur.execute("select loser as id , count(loser) as matches  from matches group by loser;")
    losses_rows = cur.fetchall()
    for i in losses_rows:
        losses[i[0]] = int(i[1])

    # use collections.Counter() to sum dictironaries
    matches = dict(Counter(wins) + Counter(losses))

    res = []
    for k, value in players.iteritems():
        res.append((k, value, wins[k] if k  in wins else 0, matches[k] if k in matches else 0))
    return res


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    sql = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    data = (winner, loser,)
    cur.execute(sql, data)
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    conn = connect()
    cur = conn.cursor()

    players = {}
    cur.execute("select id , name from players ;")
    players_rows = cur.fetchall()
    for i in players_rows:
        players[i[0]] = i[1]

    # get unique number of wins
    standings = playerStandings()
    wins = [row[2] for row in standings]
    unique_wins = list(set(wins))

    players_wins = {}
    '''generate a dictionary, key - number of wins,
    value - list of ids with the this same number of wins
    '''
    for i in unique_wins:
        wins_temp = []
        for x in standings:
            if x[2] == i:
                wins_temp.append(x[0])
        players_wins[i] = wins_temp

    result = []
    for k, players_same_wins in players_wins.iteritems():
        # for each list of players with the same number of wins
        players_random = []
        for i in range(len(players_same_wins)):
            # generate a random list
            player_choice = random.choice(players_same_wins)
            players_random.append(player_choice)
            players_same_wins.remove(player_choice)

        # generate pairings of random ids
        players_iterator = iter(players_random)
        for x, y in zip(players_iterator, players_iterator):
            result.append((x, players[x], y, players[y]))

    return result
