# Deployment

1. Create venv and install dependencies from ```requirements.txt```
2. Create the database and the user
3. Migrate the database with the command ```flask db upgrade```
4. Import the dataset with ```python import_dataset.py```
5. Run the app with ```python app.py```


# Test requests

1. Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.
```
curl --location --request POST 'http://127.0.0.1:5000/metrics' \
--header 'Content-Type: application/json' \
--data-raw '{
    "filter": {
        "date_to": "01-06-2017"
    },
    "group_by": ["channel", "country"],
    "sort": {
        "clicks": "DESC"
    }
}'
```

2. Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.
```
curl --location --request POST 'http://127.0.0.1:5000/metrics' \
--header 'Content-Type: application/json' \
--data-raw '{
    "filter": {
        "date_from": "01-05-2017",
        "date_to": "31-05-2017",
        "os": ["ios"]
    },
    "group_by": ["date"],
    "sort": {
        "date": "ASC"
    }
}'
```

3. Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.
```
curl --location --request POST 'http://127.0.0.1:5000/metrics' \
--header 'Content-Type: application/json' \
--data-raw '{
    "filter": {
        "date_from": "01-06-2017",
        "date_to": "01-06-2017",
        "country": "US",
        "os": ["ios"]
    },
    "group_by": ["os"],
    "sort": {
        "revenue": "DESC"
    }
}'
```

4. Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order. Please think carefully which is an appropriate aggregate function for CPI.
```
curl --location --request POST 'http://127.0.0.1:5000/metrics' \
--header 'Content-Type: application/json' \
--data-raw '{
    "filter": {
        "country": "CA"
    },
    "group_by": ["channel"],
    "sort": {
        "cpi": "DESC"
    }
}'
```