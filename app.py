from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Karthik37@localhost:5432/Football'

db = SQLAlchemy(app)

class LeagueStandings(db.Model):
    __tablename__ = 'epl_league_table'
    row_id = db.Column(db.Integer, primary_key=True)
    league_position = db.Column(db.Integer)
    season = db.Column(db.String(20))
    club_name = db.Column(db.String(100))
    matches_played = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    draws = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    goals_scored = db.Column(db.Integer)
    goals_conceded = db.Column(db.Integer)
    points = db.Column(db.Integer)

    def to_dict(self):
        return {
        'league_position': self.league_position,
        'season': self.season,
        'club_name': self.club_name,
        'matches_played': self.matches_played,
        'wins': self.wins,
        'draws': self.draws,
        'losses': self.losses,
        'goals_scored': self.goals_scored,
        'goals_conceded': self.goals_conceded,
        'points': self.points
    }


@app.route('/standings', methods = ['GET'])
def get_standings():
    season = request.args.get('season')
    standings_query = LeagueStandings.query

    if season:
        standings_query = standings_query.filter_by(season = season)

    standings = standings_query.all()
    return jsonify([standing.to_dict() for standing in standings])

@app.route('/standings', methods = ['POST'])
def add_standing():
    data = request.get_json()

    new_standing = LeagueStandings(
        season = data['season'],
        club_name = data['club_name'],
        matches_played = data['matches_played'],
        wins = data['wins'],
        draws = data['draws'],
        losses = data['losses'],
        goals_scored = data['goals_scored'],
        goals_conceded = data['goals_conceded'],
        points = data['points']
    )


    db.session.add(new_standing)
    db.session.commit()

    return jsonify(new_standing.to_dict()), 201



if __name__ == '__main__':
    app.run(debug=True)