import great_expectations as ge
from great_expectations.core.batch import BatchRequest
from great_expectations.exceptions import DataContextError


def create_expectations():
    context = ge.data_context.DataContext()

    # Add the datasource programmatically
    context.add_datasource(
        name="my_datasource",
        class_name="Datasource",
        execution_engine={
            "class_name": "PandasExecutionEngine",
        },
        data_connectors={
            "default_inferred_data_connector_name": {
                "class_name": "InferredAssetFilesystemDataConnector",
                "base_directory": "../data/processed/",
                "default_regex": {
                    "pattern": "(.*)\\.csv",
                    "group_names": ["data_asset_name"],
                },
            }
        },
    )

    suite_name = "default"

    # Check if the expectation suite already exists
    if suite_name in context.list_expectation_suite_names():
        print(f"Expectation suite '{suite_name}' already exists. Deleting and creating a new one.")
        context.delete_expectation_suite(expectation_suite_name=suite_name)

    # Add an expectation suite
    context.add_expectation_suite(expectation_suite_name=suite_name)

    # Define a batch request
    batch_request = BatchRequest(
        datasource_name="my_datasource",
        data_connector_name="default_inferred_data_connector_name",
        data_asset_name="my_dataset",  # Match the name from the regex pattern
    )

    try:
        # Get a batch of data
        batch = context.get_validator(
            batch_request=batch_request,
            expectation_suite_name=suite_name,
        )

        if not batch.head():
            raise ValueError("No data returned in batch. Please check the data paths and configuration.")

        # Create expectations
        batch.expect_column_to_exist("id")
        batch.expect_column_to_exist("name")
        batch.expect_column_to_exist("age")
        batch.expect_column_values_to_not_be_null("id")
        batch.expect_column_values_to_not_be_null("name")
        batch.expect_column_values_to_not_be_null("age")
        batch.expect_column_values_to_be_between("age", 0, 100)

        # Save the expectation suite
        context.save_expectation_suite(expectation_suite=batch.get_expectation_suite(),
                                       expectation_suite_name=suite_name)
        print(f"Expectation suite '{suite_name}' created successfully.")

    except DataContextError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    create_expectations()
