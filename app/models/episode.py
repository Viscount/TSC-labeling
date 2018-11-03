#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from app import db


class Episode(db.Model):
    __tablename__ = 'episode'
    av_id = db.Column(db.Integer, nullable=False)
    cid = db.Column(db.Integer, nullable=False)
    coins = db.Column(db.Integer, nullable=True)
    cover = db.Column(db.Text, nullable=True)
    episode_id = db.Column(db.Integer, primary_key=True)
    episode_status = db.Column(db.Integer, nullable=True)
    index = db.Column(db.String(32), nullable=True)
    index_title = db.Column(db.String(64), nullable=True)
    tags = db.Column(db.Text, nullable=True)
    update_time = db.Column(db.DateTime, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=True)
    updatedAt = db.Column(db.DateTime, nullable=True)
    # 外键
    season_id = db.Column(db.Integer, db.ForeignKey("bangumi.season_id"))
    bangumi = db.relationship("Bangumi", backref=db.backref("episodes", uselist=True, cascade="delete, all"))

    def __init__(self, data_dict):
        for key in data_dict:
            if hasattr(Episode, key):
                setattr(self, key, data_dict[key])
