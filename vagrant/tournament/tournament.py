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
    conn = connect()
    c = conn.cursor()
    c.execute("TRUNCATE Match;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    #Cascade those rows related to the players by foreign keys. This case, all other tables reference
    c.execute("TRUNCATE Player CASCADE;")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    #Count the number of rows in player
    c.execute("SELECT Count(Player.Id) FROM Player;")
    #Fetch return result, one row
    result = c.fetchone()
    conn.close()
    return result[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    #Add player to Player table and return id of inserted player
    c.execute("INSERT INTO Player(Name) VALUES (%s) RETURNING id", (name,))
    #Player standing must also be created after player has been inserted. Insert row with correct id
    #And default wins losses and matches to 0
    c.execute("INSERT INTO Player_Standing(Id, Wins, Losses, Matches) VALUES(%s, 0, 0, 0)", (c.fetchone()[0],))
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
    c = conn.cursor()
    #Join player and player_standing and select id, name, wins, matches from result table
    c.execute("SELECT Player.Id, Name, Wins, Matches FROM player JOIN player_standing ON player.id = player_standing.id ORDER BY Wins DESC")
    result = c.fetchall()
    conn.close()
    #Create list of tuples by iterating through fetched array and creating tuple after each iteration
    lst = []
    for row in result:
        lst.append((row[0],row[1],row[2],row[3]))

    #print lst
    return lst



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    #Record match result in match table with values passed as parameters
    c.execute("INSERT INTO Match(winnerid, loserid) VALUES (%s, %s)", (winner, loser))
    #Update the standing of the player that won by incrementing number of wins and total number of matches by one
    c.execute("UPDATE Player_standing SET wins = wins + 1, matches = matches + 1 WHERE Id = %s ", (winner,))
    #Update the standing of the player that lost by incrementing number of losses by one and total matches by one
    c.execute("UPDATE Player_standing SET losses = losses + 1, matches = matches + 1  WHERE Id = %s ", (loser,))
    conn.commit()
    conn.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
P  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    #initialize pairs list
    lstOfPairs = []
    #Use existing function to retrieve the current player standings
    standings = playerStandings()

    #Test print
    #print standings
    #print standings[::2]
    #print standings[1::2]

    #Zip together the even and odd indexed items from playerStandings() return result aka standings
    #Ex. 1,2,3,4 , even = 2,4, odd = 1,3 , zip = (1,2),(3,4)
    
    zipPairs = zip(standings[::2], standings[1::2])

    #populate list by getting data from each pair in zip pair. 
    for pair in zipPairs:
        lstOfPairs.append( (pair[0][0], pair[0][1], pair[1][0], pair[1][1]) )

    #print lstOfPairs
    #Return resulting tuple list
    return lstOfPairs

