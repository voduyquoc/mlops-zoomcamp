mlflow server --backend-store-uri=sqlite:///mlflow.db --default-artifact-root=s3://mlflow-models-quocvo/

mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://mlflow:317Hr44G6ZvG0N7iUIcm@mlflow-backend-db.ctwc2wcyo5mp.eu-north-1.rds.amazonaws.com:5432/mlflow_db --default-artifact-root s3://mlflow-models-quocvo

export RUN_ID=""