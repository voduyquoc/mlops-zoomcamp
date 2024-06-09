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

    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("homework_03")

    with mlflow.start_run():
        # Log the model
        mlflow.sklearn.log_model(lr, "linear_regression_model")
        os.makedirs('models', exist_ok=True)
        # Save the DictVectorizer as an artifact
        with open('models/linear_regression_model.bin', 'wb') as f_out:
            pickle.dump(lr, f_out)
        with open('models/dv.bin', 'wb') as f_out:
            pickle.dump(dv, f_out)
        
        mlflow.log_artifact('models/dv.bin', artifact_path="artifacts")

    


