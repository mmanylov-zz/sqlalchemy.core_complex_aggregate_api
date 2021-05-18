import os


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request
from sqlalchemy import func


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
            'date': str(self.date),
            'channel': self.channel,
            'country': self.country,
            'os': self.os,
            'impressions': self.impressions,
            'clicks': self.clicks,
            'installs': self.installs,
            'spend': self.spend,
            'revenue': self.revenue,
        }

    @staticmethod
    def get_attributes():
        return ('id', 'date', 'channel', 'country', 'os', 'impressions', 'clicks', 'installs', 'spend', 'revenue')


METRIC_ATTR_MAPPING = {
    'date': Metric.date,
    'channel': Metric.channel,
    'country': Metric.country,
    'os': Metric.os,
}


@app.route('/metrics', methods=['POST'])
def metrics_get():
    req_json = request.json
    filter_dict = req_json.get('filter')
    group_by_list = req_json.get('group_by')
    if group_by_list:
        attr_list = [v for k, v in METRIC_ATTR_MAPPING.items() if k in group_by_list]
        q = db.session.query(func.count(Metric.id), func.sum(Metric.impressions), func.sum(Metric.clicks),
                             func.sum(Metric.installs), func.sum(Metric.spend), func.sum(Metric.revenue))\
            .group_by(*attr_list)
    else:
        q = db.session.query(Metric)

    if filter_dict:
        if filter_dict.get('date_from'):
            q = q.filter(Metric.date >= filter_dict['date_from'])
        if filter_dict.get('date_to'):
            q = q.filter(Metric.date <= filter_dict['date_to'])
        if filter_dict.get('channels'):
            q = q.filter(Metric.channel.in_(filter_dict['channels']))
        if filter_dict.get('countries'):
            q = q.filter(Metric.country.in_(filter_dict['countries']))
        if filter_dict.get('os'):
            q = q.filter(Metric.os.in_(filter_dict['os']))


    # metrics = q.all()
    # metrics_dicts = [m.to_dict() for m in metrics]
    # return json.dumps(metrics_dicts)
    return f'Rows selected: {str(q.count())}\nTotal rows: {str(db.session.query(Metric).count())}'


if __name__ == '__main__':
    app.run(host="127.0.0.1")
