#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from app import db


class Bangumi(db.Model):
    __tablename__ = 'bangumi'
    cover = db.Column(db.Text, nullable=True)
    favorites = db.Column(db.Integer, nullable=True)
    is_finish = db.Column(db.Integer, nullable=True)
    newest_ep_index = db.Column(db.Integer, nullable=True)
    pub_time = db.Column(db.Integer, nullable=True)
    season_id = db.Column(db.Integer, primary_key=True)
    season_status = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(64), nullable=True)
    total_count = db.Column(db.Integer, nullable=True)
    update_time = db.Column(db.Integer, nullable=True)
    url = db.Column(db.Text, nullable=True)
    week = db.Column(db.String(30), nullable=True)
    tags = db.Column(db.Text, nullable=True)
    actors = db.Column(db.Text, nullable=True)
    createdAt = db.Column(db.DateTime, nullable=True)
    updatedAt = db.Column(db.DateTime, nullable=True)

    def __init__(self, data_dict):
        for key in data_dict:
            if hasattr(Bangumi, key):
                setattr(self, key, data_dict[key])

    def to_dict(self):
        bangumi_dict = {
            'cover': self.cover,
            'favorites': self.favorites,
            'is_finish': self.is_finish,
            'newest_ep_index': self.newest_ep_index,
            'pub_time': self.pub_time,
            'season_id': self.season_id,
            'season_status': self.season_status,
            'title': self.title,
            'total_count': self.total_count,
            'update_time': self.update_time,
            'url': self.url,
            'week': self.week,
            'tags': self.tags,
            'actors': self.actors
        }
        return bangumi_dict
