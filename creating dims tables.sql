
create table epl_league_table_dim
(	row_id numeric,
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
	etl_insert_date date,
	etl_update_date date
);

-- Merging into actual EPL table for new data
merge into epl_league_table epl
using
(select * from epl_league_table_tmp tmp) tmp
on epl.club_name = tmp.club_name
and epl.season = tmp.season
when not matched
then insert
epl.league_position = tmp.league_position
epl.club_name = tmp.club_name
epl.matches_played = tmp.matches_played
epl.wins = tmp.wins
epl.draws = tmp.draws
epl.losses = tmp.losses
epl.goals_scored = tmp.goals_scored
epl.goals_conceded = tmp.goals_conceded
epl.goal_difference = tmp.goal_difference
epl.points = tmp.points
epl.points_per_match = tmp.points_per_match
epl.xg = tmp.xg
epl.xga = tmp.xga
epl.xgd = tmp.xhd
epl.xgd_per_90 = tmp.xgd_per_90
epl.avg_attendance = tmp.avg_attendance
epl.top_team_scorer = tmp.top_team_scorer
epl.goalkeeper = tmp.goalkeeper
epl.notes = tmp.notes
epl.season = tmp.season
when matched
then update
epl.league_position = tmp.league_position
epl.club_name = tmp.club_name
epl.matches_played = tmp.matches_played
epl.wins = tmp.wins
epl.draws = tmp.draws
epl.losses = tmp.losses
epl.goals_scored = tmp.goals_scored
epl.goals_conceded = tmp.goals_conceded
epl.goal_difference = tmp.goal_difference
epl.points = tmp.points
epl.points_per_match = tmp.points_per_match
epl.xg = tmp.xg
epl.xga = tmp.xga
epl.xgd = tmp.xhd
epl.xgd_per_90 = tmp.xgd_per_90
epl.avg_attendance = tmp.avg_attendance
epl.top_team_scorer = tmp.top_team_scorer
epl.goalkeeper = tmp.goalkeeper
epl.notes = tmp.notes
epl.season = tmp.season;
