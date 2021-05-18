import os


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request
from sqlalchemy import func
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
    'impressions': Metric.impressions,
    'clicks': Metric.clicks,
    'installs': Metric.installs,
    'spend': Metric.spend,
    'revenue': Metric.revenue,
}


@app.route('/metrics', methods=['POST'])
def metrics_get():
    req_json = request.json
    filter_dict = req_json.get('filter')
    group_by_list = req_json.get('group_by')
    if group_by_list:
        attr_dict_to_group_by = {k:v for k, v in METRIC_ATTR_MAPPING.items() if k in group_by_list}
        header_row = ['count(metric.id)', 'sum(metric.impressions)', 'sum(metric.clicks)', 'sum(metric.installs)',
                      'sum(metric.spend)', 'sum(metric.revenue)']
        header_row.extend(attr_dict_to_group_by.keys())
        metric_id_count = func.count(Metric.id)
        metric_impressions_sum = func.sum(Metric.impressions)
        metric_clicks_sum = func.sum(Metric.clicks)
        metric_installs_sum = func.sum(Metric.installs)
        metric_spend_sum = func.sum(Metric.spend)
        metric_revenue_sum = func.sum(Metric.revenue)
        group_by_order_mapping = {
            'id': metric_id_count,
            'impressions': metric_impressions_sum,
            'clicks': metric_clicks_sum,
            'installs': metric_installs_sum,
            'spend': metric_spend_sum,
            'revenue': metric_revenue_sum,
            'date': Metric.date,
            'channel': Metric.channel,
            'country': Metric.country,
            'os': Metric.os
        }
        aggregates_list = [metric_id_count, metric_impressions_sum, metric_clicks_sum, metric_installs_sum,
                           metric_spend_sum, metric_revenue_sum]
        aggregates_list.extend(attr_dict_to_group_by.values())
        q = db.session.query(*aggregates_list)\
            .group_by(*attr_dict_to_group_by.values())
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

    sort_dict = req_json.get('sort')
    if sort_dict:
        if group_by_list:
            sort_list = []
            for attr, order in sort_dict.items():
                if order == 'ASC':
                    sort_list.append(group_by_order_mapping[attr].asc())
                else:
                    sort_list.append(group_by_order_mapping[attr].desc())
            if sort_list:
                q = q.order_by(*sort_list)
        else:
            sort_list = []
            for attr, order in sort_dict.items():
                if order == 'ASC':
                    sort_list.append(METRIC_ATTR_MAPPING[attr].asc())
                else:
                    sort_list.append(METRIC_ATTR_MAPPING[attr].desc())
            if sort_list:
                q = q.order_by(*sort_list)

    metrics = q.all()

    if group_by_list:
        result_list_of_dicts = []
        for m in metrics:
            result_list_of_dicts.append(dict(zip(header_row, m)))
        return json.dumps(result_list_of_dicts)
    else:
        return json.dumps([m.to_dict() for m in metrics])


if __name__ == '__main__':
    app.run(host="127.0.0.1")
