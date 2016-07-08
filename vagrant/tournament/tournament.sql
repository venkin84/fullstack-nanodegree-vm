-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players(
    playerID SERIAL PRIMARY KEY,
    playerName varchar(80) NOT NULL,
    wins integer DEFAULT 0,
    matches integer DEFAULT 0
);

CREATE TABLE matches(
    matchID SERIAL PRIMARY KEY,
    winnerID integer REFERENCES players (playerID),
    looserID integer REFERENCES players (playerID)
);
