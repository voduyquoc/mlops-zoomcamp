python -m venv venv

pip install -r requirements.txt

mlflow ui --backend-store-uri sqlite:///mlflow.db

mlflow ui

mlflow server --backend-store-uri sqlite:///backend.db


mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://DB_USER:DB_PASSWORD@DB_ENDPOINT:5432/DB_NAME --default-artifact-root s3://S3_BUCKET_NAME

mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://mlflow:K8FVjrvfOwkbq6y2073K@mlflow-backend-db.ctwc2wcyo5mp.eu-north-1.rds.amazonaws.com:5432/mlflow_db --default-artifact-root s3://mlflow-artifacts-remote-qv