from flask import Flask, request, jsonify, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import decimal
import io
from plottable import ColumnDefinition, Table
from plottable.cmap import normed_cmap
from plottable.plots import image

matplotlib.use('Agg')
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
    points_per_match = db.Column(db.Integer)
    xg = db.Column(db.Integer)
    xga = db.Column(db.Integer)
    xgd = db.Column(db.Integer)
    xgd_per_90 = db.Column(db.Integer)
    

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
        'points': self.points,
        'points_per_match': self.points_per_match,
        'xg': self.xg,
        'xga': self.xga,
        'xgd': self.xgd,
        'xgd_per_90': self.xgd_per_90
    }


@app.route('/standings', methods = ['GET'])
def get_standings():
    season = request.args.get('season')
    standings_query = LeagueStandings.query

    if season:
        standings_query = standings_query.filter_by(season = season)

    standings = standings_query.all()

    standings_list = [standing.to_dict() for standing in standings]

    standing_df = pd.DataFrame(standings_list)

    return jsonify(standings_list)

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
        points = data['points'],
        points_per_match = data['points_per_match'],
        xg = data['xg'],
        xga = data['xga'],
        xgd = data['xgd'],
        xgd_per_90 = data['xgd_per_90']
    )


    db.session.add(new_standing)
    db.session.commit()

    return jsonify(new_standing.to_dict()), 201


@app.route('/table')
def index():
    seasons = db.session.query(LeagueStandings.season).distinct().order_by(LeagueStandings.season.desc()).all()
    
    # Flatten the list of tuples into a list of strings
    seasons = [season[0] for season in seasons]
    return render_template('index.html', seasons = seasons)

@app.route('/table/plot.png')
def plot_table():
    season = request.args.get('season', '2023/2024')

    standings_query = LeagueStandings.query.filter_by(season = season).all()

    standings_list = [standing.to_dict() for standing in standings_query]

    df = pd.DataFrame(standings_list)

    if df.empty:
        return "No data available for the selected season", 404

    df = df.applymap(lambda x: float(x) if isinstance(x, decimal.Decimal) else x)

    bg_color = "#FFFFFF" # I usually just like to do a white background
    text_color = "#000000" # With black text

    row_colors = {
        "top4": "#E1FABC",
        "top6": "#FFFC97",
        "relegation": "#E79A9A",
        "even": "#E2E2E1",
        "odd": "#B3B0B0",
    }

    plt.rcParams["text.color"] = text_color
    plt.rcParams["font.family"] = "monospace"

    df['league_position'] = df['league_position'].astype(int)
    df['matches_played'] = df['matches_played'].astype(int)
    df['wins'] = df['wins'].astype(int)
    df['draws'] = df['draws'].astype(int)
    df['losses'] = df['losses'].astype(int)
    df['goals_scored'] = df['goals_scored'].astype(int)
    df['goals_conceded'] = df['goals_conceded'].astype(int)
    df['points'] = df['points'].astype(int)

    column_mapping = {
    "league_position": "Position",
    "club_name": "Club",
    "matches_played": "MP",
    "wins": "W",
    "draws": "D",
    "losses": "L",
    "goals_scored": "G",
    "goals_conceded": "GA",
    "points": "P",
    "points_per_match": "P/90",
    "xg": "xG",
    "xga": "xGA",
    "xgd": "xGD",
    "xgd_per_90": "xGD/90"
}
    df.rename(columns=column_mapping, inplace=True)
    df = df.sort_values(by = ['season', 'Position'])

    col_defs = [
    ColumnDefinition(
        name="Position",
        textprops={"ha": "center"},
        width=0.5,
    ),
    ColumnDefinition(
        name="Club",
        textprops={"ha": "left", "weight": "bold"},
        width=1.75,
    ),
    ColumnDefinition(
        name="MP",
        group="Matches Played",
        textprops={"ha": "center"},
        width=0.5,
    ),
    ColumnDefinition(
        name="W",
        group="Matches Played",
        textprops={"ha": "center"},
        width=0.5,
    ),
    ColumnDefinition(
        name="D",
        group="Matches Played",
        textprops={"ha": "center"},
        width=0.5,
    ),
    ColumnDefinition(
        name="L",
        group="Matches Played",
        textprops={"ha": "center"},
        width=0.5,
    ),
    ColumnDefinition(
        name="G",
        group="Goals",
        textprops={"ha": "center"},
        width=0.5,
    ),
    ColumnDefinition(
        name="GA",
        group="Goals",
        textprops={"ha": "center"},
        width=0.5,
    ),
    # ColumnDefinition(
    #     name="GD",
    #     group="Goals",
    #     textprops={"ha": "center"},
    #     width=0.5,
    # ),
    ColumnDefinition(
        name="P",
        group="Points",
        textprops={"ha": "center"},
        width=0.5,
    ),
    ColumnDefinition(
        name="P/90",
        group="Points",
        textprops={"ha": "center"},
        width=0.5,
    ),
    ColumnDefinition(
        name="xG",
        group="Expected Goals",
        textprops={"ha": "center", "color": "#000000", "weight": "bold", "bbox": {"boxstyle": "circle", "pad": 0.35}},
        cmap=normed_cmap(df["xG"], cmap=matplotlib.cm.PiYG, num_stds=2)
    ),
    ColumnDefinition(
        name="xGA",
        group="Expected Goals",
        textprops={"ha": "center", "color": "#000000", "weight": "bold", "bbox": {"boxstyle": "circle", "pad": 0.35}},
        cmap=normed_cmap(df["xGA"], cmap=matplotlib.cm.PiYG_r, num_stds=2)
    ),
    ColumnDefinition(
        name="xGD",
        group="Expected Goals",
        textprops={"ha": "center", "color": "#000000", "weight": "bold", "bbox": {"boxstyle": "circle", "pad": 0.35}},
        cmap=normed_cmap(df["xGD"], cmap=matplotlib.cm.PiYG, num_stds=2)
    ),
    ColumnDefinition(
        name="xGD/90",
        group="Expected Goals",
        textprops={"ha": "center", "color": "#000000", "weight": "bold", "bbox": {"boxstyle": "circle", "pad": 0.35}},
        cmap=normed_cmap(df["xGD"], cmap=matplotlib.cm.PiYG, num_stds=2)
    ),
]

    fig, ax = plt.subplots(figsize=(14, 16))
    # fig, ax = plt.subplots()
    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    table = Table(
        df,
        column_definitions=col_defs,
        index_col="Position",
        row_dividers=True,
        row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
        footer_divider=True,
        textprops={"fontsize": 14},
        col_label_divider_kw={"linewidth": 1, "linestyle": "-"},
        column_border_kw={"linewidth": .5, "linestyle": "-"},
        ax=ax,
    ).autoset_fontcolors(colnames=["xG", "xGA", "xGD", "xGD/90"]) # This will set the font color of the columns based on the cmap so the text is readable

    table.cells[10, 3].textprops["color"] = "#8ACB88"

    fig.tight_layout(pad=1.5)

    buf = io.BytesIO()
    plt.savefig(buf, format = 'png')

    buf.seek(0)
    plt.close(fig)


    return make_response(buf.getvalue()), 200, {'Content-Type': 'image/png'}


    






if __name__ == '__main__':
    app.run(debug=True)