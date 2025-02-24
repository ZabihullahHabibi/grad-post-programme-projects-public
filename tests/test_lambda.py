import json
import pytest
from unittest.mock import patch
from gdpr_obfuscator.lambda_function import lambda_handler

@patch("gdpr_obfuscator.lambda_function.process_csv")
def test_lambda_handler(mock_process):
    """Test AWS Lambda function execution."""
    event = {
        "file_to_obfuscate": "s3://test-bucket/test.csv",
        "pii_fields": ["name", "email_address"]
    }

    response = lambda_handler(event, None)
    
    expected_output_file = "s3://test-bucket/test_obfuscated.csv"
    mock_process.assert_called_once_with(event["file_to_obfuscate"], event["pii_fields"], expected_output_file)

    assert response == {"status": "success", "output_file": expected_output_file}
