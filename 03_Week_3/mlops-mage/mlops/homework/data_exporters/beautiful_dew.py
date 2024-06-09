import mlflow
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def tracking(data, *args, **kwargs):
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
    # Fetch the list of experiments
    experiments = mlflow.search_experiments()

    # Print out the experiment details
    for exp in experiments:
        print(f"Experiment Name: {exp.name}")
        print(f"Experiment ID: {exp.experiment_id}")
        print(f"Lifecycle Stage: {exp.lifecycle_stage}")
        print("-" * 20)

    # Get the size of the model file in bytes
    model_size_bytes = os.path.getsize('models/linear_regression_model.bin')
    print(model_size_bytes)