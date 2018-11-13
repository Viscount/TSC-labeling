from flask import Blueprint, render_template, abort, request, redirect, url_for
from jinja2 import TemplateNotFound
from sqlalchemy import and_
from app.models.episode import Episode
from app.models.danmaku import Danmaku
from app import db
import math
import os

episode = Blueprint('episode', __name__, template_folder='templates')


def check_attr(request):
    attr_list = ['context', 'start', 'max_sec']
    flag = True
    for attr in attr_list:
        flag = flag and (attr in request.args)
    return flag


@episode.route('/episode/<int:episode_id>', methods=['GET'])
@episode.route('/episode/<int:episode_id>/page/<int:page>', methods=['GET'])
def show_episode_danmakus(episode_id, page=1):
    try:
        if check_attr(request):
            env_args = {
                'context': int(request.args.get('context')),
                'start': int(request.args.get('start')),
                'max_sec': int(request.args.get('max_sec')),
                'page': page
            }
        else:
            danmakus = Danmaku.query.filter_by(episode_id=episode_id).order_by(Danmaku.playback_time)
            env_args = {
                'context': 5,
                'start': 0,
                'max_sec': math.ceil(danmakus[-1].playback_time),
                'page': page
            }
        episode = Episode.query.filter_by(episode_id=episode_id).first()
        start = env_args['start']
        end = env_args['start'] + env_args['context']
        danmakus_ = Danmaku.query.filter(and_(Danmaku.episode_id == episode_id,
                                            Danmaku.playback_time <= end,
                                            Danmaku.playback_time >= start)).order_by(Danmaku.playback_time).paginate(
                                            page=page, per_page=100, error_out=False)
        imgs = []
        for index in range(start, end+1):
            url = os.path.join('img', str(episode.season_id), str(episode_id), 'image-'+str('%05d' % (index+1))+'.jpeg')
            imgs.append(url)
        return render_template('episode.html', episode=episode, danmakus=danmakus_, env_args=env_args, imgs=imgs)
    except TemplateNotFound:
        abort(404)


@episode.route('/episode/<int:episode_id>/danmaku', methods=['POST'])
def set_danmakus_label(episode_id):
    try:
        env_args = {
            'context': int(request.args.get('context')),
            'start': int(request.args.get('start')),
            'max_sec': int(request.args.get('max_sec')),
            'page': int(request.args.get('page'))
        }
        form = request.form.to_dict()
        key_set = form.keys()
        danmakus = Danmaku.query.filter(Danmaku.raw_id.in_(key_set)).all()
        for danmaku in danmakus:
            raw_id = str(danmaku.raw_id)
            if form[raw_id] == '0':
                continue
            else:
                danmaku.label = int(form[raw_id])
        db.session.commit()
        return redirect(url_for('episode.show_episode_danmakus', episode_id=episode_id, page=env_args['page'],
            start=env_args['start'], context=env_args['context'], max_sec=env_args['max_sec']))
    except TemplateNotFound:
        abort(404)
