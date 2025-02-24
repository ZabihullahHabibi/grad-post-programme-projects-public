from unittest.mock import patch
from lambda_function import lambda_handler

# Patch the process_file as it is imported in lambda_function.


@patch("lambda_function.process_file")
def test_lambda_handler_csv(mock_process_file):
    event = {
        "file_to_obfuscate": "s3://bucket/data.csv",
        "pii_fields": ["name", "email"],
    }
    context = None
    result = lambda_handler(event, context)

    expected_output = "s3://bucket/data_obfuscated.csv"
    mock_process_file.assert_called_once_with(
        "s3://bucket/data.csv", ["name", "email"], expected_output
    )

    assert result["status"] == "success"  # nosec
    assert result["output_file"] == expected_output  # nosec


@patch("lambda_function.process_file")
def test_lambda_handler_json(mock_process_file):
    event = {"file_to_obfuscate": "s3://bucket/data.json", "pii_fields": ["id"]}
    context = None
    result = lambda_handler(event, context)

    expected_output = "s3://bucket/data_obfuscated.json"
    mock_process_file.assert_called_once_with(
        "s3://bucket/data.json", ["id"], expected_output
    )

    assert result["status"] == "success"  # nosec
    assert result["output_file"] == expected_output  # nosec


@patch("lambda_function.process_file")
def test_lambda_handler_parquet(mock_process_file):
    event = {"file_to_obfuscate": "s3://bucket/data.parquet", "pii_fields": ["ssn"]}
    context = None
    result = lambda_handler(event, context)

    expected_output = "s3://bucket/data_obfuscated.parquet"
    mock_process_file.assert_called_once_with(
        "s3://bucket/data.parquet", ["ssn"], expected_output
    )

    assert result["status"] == "success"  # nosec
    assert result["output_file"] == expected_output  # nosec
