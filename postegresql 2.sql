select * from epl_league_table_tmp;

select * from epl_league_table_tmp_no_xg
limit 10;

select * from epl_league_table;


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
