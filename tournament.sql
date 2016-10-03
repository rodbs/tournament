-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- execute 
-- psql -f tournament.sql 
-- to run the script

drop database if exists tournament;
create database tournament;

\c tournament 

create table players (id SERIAL primary key, name text);
create table matches (matchId SERIAl, winner integer references players(id), loser  integer references players(id));

create  view v_wins as select winner as id , count(winner) as matches  from matches group by winner;
create or replace view v_losses as select loser as id , count(loser) as matches from matches group by loser;
