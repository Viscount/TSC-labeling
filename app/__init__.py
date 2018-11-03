from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

# create and configure the app
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI='mysql://root:admin@127.0.0.1:3306/danmaku',
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
)
Bootstrap(app)
db = SQLAlchemy(app)

from app.models.bangumi import Bangumi
from app.models.episode import Episode
from app.models.danmaku import Danmaku
from app.filter import playback_formation
from app.season import season
from app.episode import episode

db.init_app(app)
db.create_all(app=app)

app.register_blueprint(season)
app.register_blueprint(episode)
