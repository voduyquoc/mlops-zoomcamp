import sys
import pandas as pd
from datetime import datetime

import batch

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

year = int(sys.argv[1])
month = int(sys.argv[2])

data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
]

columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df_input = pd.DataFrame(data, columns=columns)
print('df_input:')
print(df_input)

S3_ENDPOINT_URL = 'http://localhost:4566'

options = {
'client_kwargs': {
    'endpoint_url': S3_ENDPOINT_URL
    }
}

input_file = batch.get_input_path(year, month)
print(f'input_path: {input_file}')
batch.save_data(df_input, input_file, options)
print('save file to s3 ...')

