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
CREATE TABLE IF NOT EXISTS players (
	playerid	SERIAL,
	name		varchar(40) NOT NULL,
	date_added	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	active		integer,
	win		integer,
	total_matches	integer,
	PRIMARY KEY (playerid)
);
CREATE TABLE IF NOT EXISTS matches (
	matchid		SERIAL,
	playerid	integer REFERENCES players,
	win		integer,
	loss		integer,
	place		integer,
	champion	integer,
	bye		integer,
	PRIMARY KEY (matchid, playerid)
);
CREATE TABLE IF NOT EXISTS stats (
	playerid	integer NOT NULL REFERENCES players,
	tournament_wins	integer,
	game_wins	integer,
	PRIMARY KEY (playerid)
);
