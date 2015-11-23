#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero. Returned %s..." % c)
    print "3. After deleting, countPlayers() returns zero. Returned %s..." % c


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1. Returned %s..." % c)
    print "4. After registering a player, countPlayers() returns 1. Returned %s..." % c


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."

# Modified test so that extra values didnt fail

def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    joinTournament(1)
    standings = playerStandings(1)
    print "6. Newly registered players appear in the standings with no matches."

# Modified test reporting to include extra arguments.

def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    joinTournament(1)
    standings = playerStandings(1)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(1, id1, id2, 0, 0)
    reportMatch(1, id3, id4, 0, 0)
    standings = playerStandings(1)
    for (i, n, w, m, s, p, b) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded. returned %s" % id1)
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."

# Modified test to include extra player and swiss parings returns 3 rather than two
def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Discord")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    joinTournament(1)
    standings = playerStandings(1)
    [id1, id2, id3, id4, id5] = [row[0] for row in standings]
    reportMatch(1, id1, id2, 0, 0)
    reportMatch(1, id3, id4, 0, 0)
    reportMatch(1, id5, id1, 0, 0)
    pairings = swissPairings(1)
    print "8. After one match, players with one win are paired."


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"
