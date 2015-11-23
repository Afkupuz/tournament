# coding: utf-8
#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

# Imported time incase I need to fetch the date someone joing

import time

# Import psycopg2 to connect to psql database

import psycopg2


# dbc (data base connect) defines the database for all other methods

def dbc():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect('dbname=tournament')

# removes all matches

def deleteMatches():
    """Remove all the match records from the database."""
    DB = dbc()
    DB.cursor().execute('DELETE FROM matches')
    DB.commit()
    DB.close()

# removes all players

def deletePlayers():
    """Remove all the player records from the database."""
    DB = dbc()
    DB.cursor().execute('DELETE FROM players')
    DB.commit()
    DB.close()

# returns the total count of active players

def countPlayers():
    """Returns the number of players currently registered."""
    DB = dbc()
    c = DB.cursor()
    c.execute('SELECT COUNT(*) from players WHERE active = 1')
    total = c.fetchone()
    DB.close()
    return int(total[0])

# adds player to the database safely

def registerPlayer(name):
    """Adds a player to the tournament database.
        
        The database assigns a unique serial id number for the player.  (This
        should be handled by your SQL database schema, not in your Python code.)
        
        Args:
        name: the player's full name (need not be unique).
        """
    DB = dbc()
    DB.cursor().execute(('INSERT INTO players (name)\
                         VALUES (%s)'), (name,))
    DB.commit()
    DB.close()

# Allows active players to join X tournament

def joinTournament(matchid):
    # matchid = 1
    DB = dbc()
    c = DB.cursor()
    c.execute('INSERT INTO matches (playerid) \
               SELECT playerid from players \
               WHERE active = 1')
    c.execute(('UPDATE matches \
              SET matchid = %s \
              WHERE matchid = 0'), (matchid,))
    DB.commit()
    DB.close()

# re-orders players with most wins at the top and returns list
# argument defines which tournament is requested

def playerStandings(matchid):
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
    DB = dbc()
    c = DB.cursor()
    c.execute('SELECT matches.playerid, name, win, total_matches, \
              score, played, bye \
              FROM matches JOIN players \
              ON matches.playerid = players.playerid \
              WHERE matches.matchid = %s \
              ORDER BY matches.score DESC', (matchid,))
    player_stats = c.fetchall()
    DB.close()
    return player_stats

# grants points to winners, losers, ties, and byes depending
# on what matchid or tournament
# also update wins and matches, and regesters bye and played against

def reportMatch(matchid, winner, loser, tie , bye):
    """Records the outcome of a single match between two players.
        Args:
        winner:  the id number of the player who won
        loser:  the id number of the player who lost
        """
    DB = dbc()
    c = DB.cursor()
    if bye != 0:
        c.execute('UPDATE matches \
                  SET win = (win+1), \
                  total_matches = (total_matches+1), \
                  score = (score+3), \
                  bye = 1 \
                  WHERE playerid = %s AND matchid = %s', (bye, matchid))
    if tie == 1:
        c.execute('UPDATE matches \
                  SET total_matches = (total_matches+1), \
                  score = (score+1), \
                  played = array_append(played, %s) \
                  WHERE playerid = %s AND matchid = %s', (loser, winner, matchid))
        c.execute('UPDATE matches \
                  SET total_matches = (total_matches+1), \
                  score = (score+1), \
                  played = array_append(played, %s) \
                  WHERE playerid = %s AND matchid = %s', (winner, loser, matchid))
    elif tie == 0:
        c.execute('UPDATE matches \
                  SET win = (win+1), \
                  total_matches = (total_matches+1), \
                  score = (score+3), \
                  played = array_append(played, %s) \
                  WHERE playerid = %s AND matchid = %s', (loser, winner, matchid))
        c.execute('UPDATE matches \
                  SET total_matches = (total_matches+1), \
                  score = (score+0), \
                  played = array_append(played, %s) \
                  WHERE playerid = %s AND matchid = %s', (winner, loser, matchid))
    DB.commit()
    DB.close()

# determines which two players should battle next

def swissPairings(matchid):
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
    standings = playerStandings(matchid)
    matchup = []
    """
    # if statement pops out player who hasnt had a bye yet
    # bye chosen from middle ranked players
    if len(standings)%2 != 0:
        bye_place = len(standings)/2
        while (standings[bye_place][6] == 1):
            bye_place = bye_place + 1
        bye = standings.pop(bye_place)
    #build match-up system
    for num in range(0, len(standings)):
        if num%2 == 0:
            matches.append(num)
    """
    while (len(standings) != 0):
        to_match = standings.pop(0)
        next_player = 0
        print "to match"
        while (to_match[0] in standings[next_player][5]):
            print "next player"
            next_player = next_player + 1
        matched = standings.pop(next_player)
        matchup.append((to_match[0], to_match[1],
                        matched[0], matched[1]))
        if (len(standings) == 1):
            bye = standings.pop(0)
            matchup.append((bye[0],bye[1]))
    return matchup
