#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    dbConnection = connect()
    cursor = dbConnection.cursor()
    q1 = "DELETE FROM matches;"
    cursor.execute(q1)
    q2 = "UPDATE players SET matches = 0, wins = 0;"
    cursor.execute(q2)
    try:
        dbConnection.commit()
        dbConnection.close()
    except psycopg2.Error as e:
        return e
    return True

def deletePlayers():
    """Remove all the player records from the database."""
    dbConnection = connect()
    cursor = dbConnection.cursor()
    q = "DELETE FROM players;"
    cursor.execute(q)
    try:
        dbConnection.commit()
        dbConnection.close()
    except psycopg2.Error as e:
        return e
    return True


def countPlayers():
    """Returns the number of players currently registered."""
    dbConnection = connect()
    cursor = dbConnection.cursor()
    q = "SELECT COUNT(*) FROM players;"
    cursor.execute(q)
    count = cursor.fetchone()
    try:
        dbConnection.commit()
        dbConnection.close()
    except psycopg2.Error as e:
        return e
    return count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    dbConnection = connect()
    cursor = dbConnection.cursor()
    q = "INSERT INTO players (playerName) VALUES (%s);"
    cursor.execute(q, (name,))
    try:
        dbConnection.commit()
        dbConnection.close()
    except psycopg2.Error as e:
        return e
    return True

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
    dbConnection = connect()
    cursor = dbConnection.cursor()
    q = "SELECT * FROM players ORDER BY wins DESC;"
    cursor.execute(q)
    players = cursor.fetchall()
    try:
        dbConnection.commit()
        dbConnection.close()
    except psycopg2.Error as e:
        return e
    return players

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    dbConnection = connect()
    cursor = dbConnection.cursor()
    q1 = "INSERT INTO matches (winnerID, looserID) VALUES (%s, %s);"
    cursor.execute(q1, (winner, loser,))
    q2 = "UPDATE players SET wins = wins + 1 WHERE playerID = %s;"
    cursor.execute(q2, (winner,))
    q3 = "UPDATE players SET matches = matches + 1 WHERE playerID = %s OR playerID = %s;"
    cursor.execute(q3, (winner, loser,))
    try:
        dbConnection.commit()
        dbConnection.close()
    except psycopg2.Error as e:
        return e
    return True

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
