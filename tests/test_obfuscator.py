import pytest
import pandas as pd
from io import BytesIO
from unittest.mock import patch, MagicMock
from gdpr_obfuscator.obfuscator import load_csv_from_s3, obfuscate_pii, save_csv_to_s3

@pytest.fixture
def sample_dataframe():
    """Returns a sample DataFrame for testing."""
    data = {
        "student_id": [1234],
        "name": ["John Smith"],
        "course": ["Software"],
        "graduation_date": ["2024-03-31"],
        "email_address": ["j.smith@email.com"]
    }
    return pd.DataFrame(data)

@patch("gdpr_obfuscator.obfuscator.boto3.client")
def test_load_csv_from_s3(mock_boto3):
    """Test loading a CSV file from S3 into a DataFrame."""
    mock_s3 = mock_boto3.return_value
    sample_csv = b"student_id,name,course,graduation_date,email_address\n1234,John Smith,Software,2024-03-31,j.smith@email.com"  # Use bytes

    mock_s3.get_object.return_value = {"Body": BytesIO(sample_csv)}  # Return BytesIO
    
    df = load_csv_from_s3("s3://test-bucket/test.csv")
    
    assert not df.empty
    assert list(df.columns) == ["student_id", "name", "course", "graduation_date", "email_address"]
    assert df.loc[0, "name"] == "John Smith"

def test_obfuscate_pii(sample_dataframe):
    """Test that the PII fields are obfuscated."""
    pii_fields = ["name", "email_address"]
    obfuscated_df = obfuscate_pii(sample_dataframe, pii_fields)

    assert obfuscated_df["name"].iloc[0] == "***"
    assert obfuscated_df["email_address"].iloc[0] == "***"
    assert obfuscated_df["course"].iloc[0] == "Software"  # Non-PII fields remain unchanged

@patch("gdpr_obfuscator.obfuscator.boto3.client")
def test_save_csv_to_s3(mock_boto3, sample_dataframe):
    """Test saving a DataFrame to S3 as a CSV."""
    mock_s3 = mock_boto3.return_value

    save_csv_to_s3(sample_dataframe, "s3://test-bucket/obfuscated.csv")
    
    mock_s3.put_object.assert_called_once()
    args, kwargs = mock_s3.put_object.call_args
    assert kwargs["Bucket"] == "test-bucket"
    assert "obfuscated.csv" in kwargs["Key"]
    assert "John Smith" in kwargs["Body"].decode()

