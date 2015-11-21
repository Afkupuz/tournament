# coding: utf-8
#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import time
import psycopg2
import bleach

# conncect defines the database for all other methods

def conncect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect('dbname=tournament')

# deleteMatches removes all match records

def deleteMatches():
    """Remove all the match records from the database."""
    DB = conncect()
    DB.cursor().execute('DELETE FROM matches')
    DB.commit()
    DB.close()

# removes players

def deletePlayers():
    """Remove all the player records from the database."""
    DB = conncect()
    DB.cursor().execute('DELETE FROM players')
    DB.commit()
    DB.close()

# returns the total count of regestered players

def countPlayers():
    """Returns the number of players currently registered."""
    DB = conncect()
    c = DB.cursor()
    c.execute('SELECT COUNT(*) from players')
    total_players = c.fetchone()
    DB.close()
    return int(total_players[0])

# adds player to the database and cleans entry

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = conncect()
    clean = bleach.clean(name)
    DB.cursor().execute(('INSERT INTO players (name, active, win, total_matches)\
                         VALUES (%s, %s, %s, %s)'), (clean, 1, 0, 0))
    DB.commit()
    DB.close()

# re-orders players with most wins at the top and returns list

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
    DB = conncect()
    c = DB.cursor()
    c.execute('SELECT playerid, name, win, total_matches FROM players \
              ORDER BY win DESC')
    player_stats = c.fetchall()
    DB.close()
    return player_stats

# determines winner and loser and adds a match point

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = conncect()
    c = DB.cursor()
    c.execute('UPDATE players \
              SET win = (win+1), \
              total_matches = (total_matches+1)  \
              WHERE playerid = (%s)' % winner)
    c.execute('UPDATE players \
              SET total_matches = (total_matches+1)  \
              WHERE playerid = (%s)' % loser)
    DB.commit()
    DB.close()
 
# determines which two players should battle next

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
    standings = playerStandings()
    matches = []
    matchup = []
    if len(standings)%2 != 0:
        DB = conncect()
        c = DB.cursor()
        bye_place = len(standings) / 2
        bye = standings.pop(bye_place)
        c.execute('UPDATE players \
                  SET win = (win+1), \
                  total_matches = (total_matches+1)  \
                  WHERE playerid = (%s)' % bye[0])
        DB.commit()
        DB.close()
    for num in range(0, len(standings)):
        if num%2 == 0:
            matches.append(num)
    for num in matches:
        matchup.append((standings[num][0], standings[num][1],
                       standings[num+1][0], standings[num+1][1]))
    return matchup
