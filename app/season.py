from flask import Blueprint, render_template, abort, jsonify
from jinja2 import TemplateNotFound
from app.models.bangumi import Bangumi
from app.models.episode import Episode
from app import app
import os

season = Blueprint('season', __name__, template_folder='templates')


@season.route('/', methods=['GET'])
@season.route('/seasons', methods=['GET'])
def show_all_seasons():
    try:
        seasons = Bangumi.query.all()
        has_img = dict()
        for season in seasons:
            if os.path.isdir(os.path.join(app.root_path, 'static/img/'+str(season.season_id))):
                has_img[season.season_id] = True
            else:
                has_img[season.season_id] = False
        return render_template('index.html', seasons=seasons, has_img=has_img)
    except TemplateNotFound:
        abort(404)


@season.route('/season/<int:season_id>', methods=['GET'])
def show_season_episodes(season_id):
    try:
        season = Bangumi.query.filter_by(season_id=season_id).first()
        episodes = Episode.query.filter_by(season_id=season_id).all()
        return render_template('season.html', season=season, episodes=episodes)
    except TemplateNotFound:
        abort(404)
