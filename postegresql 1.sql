create table epl_league_table_tmp
(
	league_position numeric(2),
	club_name varchar(255),
	matches_played numeric(2),
	wins numeric(2),
	draws numeric(2),
	losses numeric(2),
	goals_scored numeric(10),
	goals_conceded numeric(10),
	goal_difference numeric(10),
	points numeric(3),
	points_per_match numeric,
	xG numeric,
	xGA numeric,
	xGD numeric,
	xGD_per_90 numeric,
	avg_attendance numeric(10),
	top_team_scorer varchar(255),
	goalkeeper varchar(255),
	notes varchar,
	season text
);



select distinct season from epl_leagueś_table_tmp
order by season;

select distinct season from epl_league_table_tmp_no_xg
order by season desc;

select * from information_schema.tables

-- truncate epl_league_table_tmp;

-- drop table epl_league_table_tmp;

-- country, league, etl_insert_dt, etl_update_dt, datasource

CREATE SEQUENCE seq_epl_league_table INCREMENT BY 1 MINVALUE 1 START 1 NO CYCLE;


create table epl_league_table
(	row_id numeric default nextval('seq_epl_league_table'),
	league_position numeric(2),
	club_name varchar(255),
	matches_played numeric(2),
	wins numeric(2),
	draws numeric(2),
	losses numeric(2),
	goals_scored numeric(10),
	goals_conceded numeric(10),
	goal_difference numeric(10),
	points numeric(3),
	points_per_match numeric,
	xG numeric,
	xGA numeric,
	xGD numeric,
	xGD_per_90 numeric,
	avg_attendance numeric(10),
	top_team_scorer varchar(255),
	goalkeeper varchar(255),
	notes varchar,
	season text,
	country varchar,
	continent varchar,
	league_tier varchar,
	gender varchar,
	datasource varchar,
	etl_insert_date date default CURRENT_TIMESTAMP,
	etl_update_date date default CURRENT_TIMESTAMP
);