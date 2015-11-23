-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop database if it already exists so that we ensure everything is fresh and correct

DROP DATABASE IF EXISTS tournament;

-- Create database

CREATE DATABASE tournament;

-- connect to database

\c tournament;

-- create tables and define their units, and relationships
-- players contain player names, their start date and if they are active

CREATE TABLE players (
	playerid	SERIAL,
	name		text NOT NULL,
	date_added	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	active		integer DEFAULT 1,
	PRIMARY KEY (playerid)
);

-- matches are organized by matchid and players can join a matchid
-- this allows multiple tournaments with different matchids

CREATE TABLE matches (
	matchid		integer DEFAULT 0,
	playerid	integer REFERENCES players,
	win		integer DEFAULT 0,
	total_matches	integer DEFAULT 0,
	score		integer DEFAULT 0,
	played		integer[],
	bye		integer DEFAULT 0,
	PRIMARY KEY (matchid, playerid)
);
