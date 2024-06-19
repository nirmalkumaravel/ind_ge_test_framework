import great_expectations as ge
from great_expectations.checkpoint import SimpleCheckpoint

def validate_data():
    context = ge.data_context.DataContext()

    checkpoint_config = {
        "name": "my_checkpoint",
        "config_version": 1.0,
        "class_name": "SimpleCheckpoint",
        "batches": [
            {
                "batch_kwargs": {
                    "path": "data/processed/my_dataset.csv",
                    "datasource": "my_datasource"
                },
                "expectation_suite_names": ["default"]
            }
        ]
    }
    context.add_checkpoint(**checkpoint_config)
    results = context.run_checkpoint(checkpoint_name="my_checkpoint")
    return results

if __name__ == "__main__":
    validation_results = validate_data()
    print(validation_results)
