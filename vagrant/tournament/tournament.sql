-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE Tournament;
\c tournament;

CREATE TABLE Player(
    ID serial primary key,
    Name varchar(50) not null
);

CREATE TABLE Player_Standing(
    ID serial references Player(ID),
    Wins int not null,
    Losses int not null,
    Matches int not null
);

CREATE TABLE Match(
    ID serial primary key,
    WinnerID serial references Player(ID),
    LoserID serial references Player(ID)
);
    
