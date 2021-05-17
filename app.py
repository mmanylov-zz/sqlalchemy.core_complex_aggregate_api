import os

from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request
import json


app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    channel = db.Column(db.String(256), nullable=False)
    country = db.Column(db.String(256), nullable=False)
    os = db.Column(db.String(256), nullable=False)
    impressions = db.Column(db.Integer, nullable=False)
    clicks = db.Column(db.Integer, nullable=False)
    installs = db.Column(db.Integer, nullable=False)
    spend = db.Column(db.Float, nullable=False)
    revenue = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Metric id={} date={}>'.format(self.id, str(self.date))

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'channel': self.channel,
            'country': self.country,
            'os': self.os,
            'impressions': self.impressions,
            'clicks': self.clicks,
            'installs': self.installs,
            'spend': self.spend,
            'revenue': self.revenue,
        }


@app.route('/metrics', methods=['POST'])
def metrics_get():
    req_json = request.json
    filter = req_json.get('filter')
    if filter:
        pass
    metrics = []
    return json.dumps(metrics)


if __name__ == '__main__':
    app.run(host="127.0.0.1")
