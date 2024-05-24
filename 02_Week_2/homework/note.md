01. mlflow --version
mlflow, version 2.13.0

02. python preprocess_data.py --raw_data_path ./data --dest_path ./output
4

03. python train.py
2

04. mlflow server --backend-store-uri sqlite:///backend.db --default-artifact-root ./artifacts
default-artifact-root

05. python hpo.py
5.335

06. python register_model.py
5.567