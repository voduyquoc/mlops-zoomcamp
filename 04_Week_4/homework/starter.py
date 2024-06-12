#!/usr/bin/env python
# coding: utf-8

import sys
import pickle
import pandas as pd


def read_data(filename, year, month):
    df = pd.read_parquet(filename)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def prepare_dictionaries(df: pd.DataFrame):
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    dicts = df[categorical].to_dict(orient='records')
    return dicts

def load_model(model_path: str):
    with open(model_path, 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return dv, model

def save_results(df, y_pred, output_file):
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred
    print(f'the mean predicted duration: {df_result.predicted_duration.mean():.2f} ...')
    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )   

def get_paths(year, month):
    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'output_{year:04d}-{month:02d}.parquet'
    return input_file, output_file

def apply_model(input_file, output_file, model_path, year, month):
    df = read_data(input_file, year, month)
    dicts = prepare_dictionaries(df)
    dv, model = load_model(model_path)
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    save_results(df, y_pred, output_file)
    return output_file

def ride_duration_prediction(year, month, model_path):
    input_file, output_file = get_paths(year, month)

    apply_model(
        input_file=input_file,
        output_file=output_file,
        model_path=model_path,
        year=year,
        month=month
    )

def run():
    year = int(sys.argv[1]) # 2023
    month = int(sys.argv[2]) # 4
    model_path = 'model.bin'
    print(f'predict the taxi duration for the {year:04d}-{month:02d} yellow data ...')
    ride_duration_prediction(year=year, month=month, model_path=model_path)


if __name__ == '__main__':
    run()


