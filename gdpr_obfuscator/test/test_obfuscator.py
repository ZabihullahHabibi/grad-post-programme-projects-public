import pytest
import pandas as pd
from io import BytesIO
from unittest.mock import patch

from gdpr_obfuscator.gdpr_obfuscator.obfuscator import (
    load_csv_from_s3,
    obfuscate_pii,
    save_csv_to_s3,
    process_csv,
)


@pytest.fixture
def sample_dataframe():
    """Returns a sample DataFrame for testing."""
    data = {
        "student_id": [1234],
        "name": ["John Smith"],
        "course": ["Software"],
        "graduation_date": ["2024-03-31"],
        "email_address": ["j.smith@email.com"],
    }
    return pd.DataFrame(data)


@patch("gdpr_obfuscator.gdpr_obfuscator.obfuscator.boto3.client")
def test_load_csv_from_s3(mock_boto_client):
    """Test loading a CSV file from S3 into a DataFrame."""
    mock_s3 = mock_boto_client.return_value
    sample_csv = b"student_id,name,course,graduation_date,email_address\n1234,John Smith,Software,2024-03-31,j.smith@email.com"
    mock_s3.get_object.return_value = {"Body": BytesIO(sample_csv)}

    df = load_csv_from_s3("s3://test-bucket/test.csv")

    assert not df.empty # nosec
    assert list(df.columns) == [
        "student_id",
        "name",
        "course",
        "graduation_date",
        "email_address",
    ] # nosec
    assert df.loc[0, "name"] == "John Smith" # nosec


def test_obfuscate_pii(sample_dataframe):
    """Test that the PII fields are obfuscated."""
    pii_fields = ["name", "email_address"]
    obfuscated_df = obfuscate_pii(sample_dataframe, pii_fields)

    assert obfuscated_df["name"].iloc[0] == "***" # nosec
    assert obfuscated_df["email_address"].iloc[0] == "***" # nosec
    # Non-PII field remains unchanged
    assert obfuscated_df["course"].iloc[0] == "Software" # nosec


@patch("gdpr_obfuscator.gdpr_obfuscator.obfuscator.boto3.client")
def test_save_csv_to_s3(mock_boto_client, sample_dataframe):
    """Test saving a DataFrame to S3 as a CSV."""
    mock_s3 = mock_boto_client.return_value
    save_csv_to_s3(sample_dataframe, "s3://test-bucket/obfuscated.csv")

    mock_s3.put_object.assert_called_once()
    args, kwargs = mock_s3.put_object.call_args
    assert kwargs["Bucket"] == "test-bucket" # nosec
    assert "obfuscated.csv" in kwargs["Key"] # nosec
    # Validate that the CSV content contains the sample data
    assert "John Smith" in kwargs["Body"].decode() # nosec


@patch("gdpr_obfuscator.gdpr_obfuscator.obfuscator.load_csv_from_s3")
@patch("gdpr_obfuscator.gdpr_obfuscator.obfuscator.save_csv_to_s3")
def test_process_csv(mock_save, mock_load, sample_dataframe):
    """Test the full obfuscation process from S3 loading to saving."""
    mock_load.return_value = sample_dataframe

    process_csv(
        "s3://test-bucket/input.csv",
        ["name", "email_address"],
        "s3://test-bucket/output.csv",
    )

    mock_load.assert_called_once_with(
        "s3://test-bucket/input.csv", endpoint_url=None)
    mock_save.assert_called_once()
