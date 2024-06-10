import mlflow
import mlflow.sklearn
import pickle
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    dv, lr = data
    os.makedirs("models", exist_ok=True)
    with open("models/dict_vectorizer.b", "wb") as f_out:
        pickle.dump(dv, f_out)

    mlflow.set_tracking_uri("http://mlflow:5000")

    # Ensure there are no active runs
    if mlflow.active_run():
        mlflow.end_run()

    mlflow.set_experiment("homework_03")

    with mlflow.start_run() as run:
        # Log model
        mlflow.sklearn.log_model(lr, "artifacts")
        # Optionally log other artifacts
        mlflow.log_artifact("models/dict_vectorizer.b", artifact_path="preprocessor")
        print(f"Model logged with run_id: {run.info.run_id}")

    


