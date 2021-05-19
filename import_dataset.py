import csv
from app import Metric, db


with open('dataset.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    metrics = []
    for row in csv_reader:
        line_count += 1
        metrics.append(Metric(
            date=row['date'],
            channel=row['channel'],
            country=row['country'],
            os=row['os'],
            impressions=row['impressions'],
            clicks=row['clicks'],
            installs=row['installs'],
            spend=row['spend'],
            revenue=row['revenue'],
        ))
    db.session.bulk_save_objects(metrics)
    db.session.commit()
    print(f'Processed {line_count} lines.')

