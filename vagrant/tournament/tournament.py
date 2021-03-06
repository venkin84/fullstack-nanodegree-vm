#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    dbConnection = psycopg2.connect("dbname=tournament")
    cursor = dbConnection.cursor()
    return dbConnection, cursor


def deleteMatches():
    """Remove all the match records from the database."""
    dbConnection, cursor = connect()
    q = "DELETE FROM matches;"
    cursor.execute(q)
    try:
        dbConnection.commit()
        dbConnection.close()
    except psycopg2.Error as e:
        return e
    return True


def deletePlayers():
    """Remove all the player records from the database."""
    dbConnection, cursor = connect()
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
    dbConnection, cursor = connect()
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

    dbConnection, cursor = connect()
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

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    dbConnection, cursor = connect()
    q = "SELECT * FROM standings;"
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
    dbConnection, cursor = connect()
    q = "INSERT INTO matches (winnerID, looserID) VALUES (%s, %s);"
    cursor.execute(q, (winner, loser,))
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
    dbConnection, cursor = connect()
    q = "SELECT * FROM standings;"
    cursor.execute(q)
    players = cursor.fetchall()
    pairs = []
    pair = []
    for i in range(0, len(players), 2):
        pair = [players[i][0], players[i][1], players[i+1][0], players[i+1][1]]
        pairs.append(pair)
    try:
        dbConnection.commit()
        dbConnection.close()
    except psycopg2.Error as e:
        return e
    return pairs
