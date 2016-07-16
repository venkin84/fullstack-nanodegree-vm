-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players(
    playerID SERIAL PRIMARY KEY,
    playerName varchar(80) NOT NULL
);

CREATE TABLE matches(
    matchID SERIAL PRIMARY KEY,
    winnerID integer REFERENCES players (playerID),
    looserID integer REFERENCES players (playerID)
);

CREATE VIEW standings AS
    SELECT players.playerID as id, players.playerName as name, winCount.wins as wins, matchCount.matches as matches
        FROM
            players,
            (SELECT players.playerID as player, COUNT(matches.winnerID) as wins
                FROM players LEFT JOIN matches ON
                    players.playerID = matches.winnerID
                GROUP BY players.playerID) as winCount,
            (SELECT players.playerID as player, COUNT(matches) as matches
                FROM players LEFT JOIN matches ON
                    players.playerID = matches.winnerID OR
                    players.playerID = matches.looserID
                GROUP BY players.playerID) as matchCount
        WHERE
            players.playerID = winCount.player AND
            players.playerID = matchCount.player
        ORDER BY wins DESC;
