import pytest
import pandas as pd
from io import StringIO
from unittest.mock import patch, MagicMock
from gdpr_obfuscator.obfuscator import load_csv_from_s3

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
    sample_csv = "student_id,name,course,graduation_date,email_address\n1234,John Smith,Software,2024-03-31,j.smith@email.com"

    mock_s3.get_object.return_value = {"Body": StringIO(sample_csv)}
    
    df = load_csv_from_s3("s3://test-bucket/test.csv")
    
    assert not df.empty
    assert list(df.columns) == ["student_id", "name", "course", "graduation_date", "email_address"]
    assert df.loc[0, "name"] == "John Smith"