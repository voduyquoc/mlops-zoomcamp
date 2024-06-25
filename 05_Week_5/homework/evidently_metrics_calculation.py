import datetime
import time
import logging
import pandas as pd
import psycopg

from prefect import task, flow

from evidently.report import Report
from evidently.metrics import ColumnQuantileMetric

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = 10

create_table_statement = """
drop table if exists homework_metrics;
create table homework_metrics(
	timestamp timestamp,
	quantile_daily float)
"""

raw_data = pd.read_parquet('data/green_tripdata_2024-03.parquet')

begin = datetime.datetime(2024, 3, 1, 0, 0)

report = Report(metrics=[ColumnQuantileMetric(column_name="fare_amount", quantile=0.5)])

@task
def prep_db():
	with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
		if len(res.fetchall()) == 0:
			conn.execute("create database test;")
		with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example") as conn:
			conn.execute(create_table_statement)

@task
def calculate_metrics_postgresql(curr, i):
	current_data = raw_data[(raw_data.lpep_pickup_datetime >= (begin + datetime.timedelta(i))) &
		(raw_data.lpep_pickup_datetime < (begin + datetime.timedelta(i + 1)))]

	report.run(current_data = current_data, reference_data = current_data)

	result = report.as_dict()

	quantile_daily = result['metrics'][0]['result']['current']['value'].item()

	curr.execute(
		"insert into homework_metrics(timestamp, quantile_daily) values (%s, %s)",
		(begin + datetime.timedelta(i), quantile_daily)
	)

@flow
def batch_monitoring_backfill():
	prep_db()
	last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
	with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example", autocommit=True) as conn:
		for i in range(0, 31):
			with conn.cursor() as curr:
				calculate_metrics_postgresql(curr, i)

			new_send = datetime.datetime.now()
			seconds_elapsed = (new_send - last_send).total_seconds()
			if seconds_elapsed < SEND_TIMEOUT:
				time.sleep(SEND_TIMEOUT - seconds_elapsed)
			while last_send < new_send:
				last_send = last_send + datetime.timedelta(seconds=10)
			logging.info("data sent")

if __name__ == '__main__':
	batch_monitoring_backfill()
