from flask import Blueprint, render_template, abort, jsonify
from jinja2 import TemplateNotFound
from app.models.bangumi import Bangumi
from app.models.episode import Episode
from app.models.danmaku import Danmaku
from app import app
import os

season = Blueprint('season', __name__, template_folder='templates')


@season.route('/', methods=['GET'])
@season.route('/seasons', methods=['GET'])
def show_all_seasons():
    try:
        seasons = Bangumi.query.all()
        has_img = dict()
        episode_counts = dict()
        for season in seasons:
            count = Episode.query.filter_by(season_id=season.season_id).count()
            episode_counts[season.season_id] = count
            if os.path.isdir(os.path.join(app.root_path, 'static/img/'+str(season.season_id))):
                has_img[season.season_id] = True
            else:
                has_img[season.season_id] = False
        return render_template('index.html', seasons=seasons, has_img=has_img, episode_counts=episode_counts)
    except TemplateNotFound:
        abort(404)


@season.route('/season/<int:season_id>', methods=['GET'])
def show_season_episodes(season_id):
    try:
        season = Bangumi.query.filter_by(season_id=season_id).first()
        episodes = Episode.query.filter_by(season_id=season_id).all()
        danmaku_counts = dict()
        tot_danmaku = 0
        for episode in episodes:
            count = Danmaku.query.filter_by(episode_id=episode.episode_id).count()
            danmaku_counts[episode.episode_id] = count
            tot_danmaku += count
        return render_template('season.html', season=season, episodes=episodes,
                               danmaku_counts=danmaku_counts, tot_danmaku=tot_danmaku)
    except TemplateNotFound:
        abort(404)
