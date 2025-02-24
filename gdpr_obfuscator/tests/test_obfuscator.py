from io import BytesIO
import pandas as pd
from unittest.mock import patch, MagicMock

from gdpr_obfuscator.obfuscator import (
    load_file_from_s3,
    save_file_to_s3,
    process_file,
    obfuscate_pii,
)


def test_obfuscate_pii():
    df = pd.DataFrame(
        {"name": ["John Doe"], "email": ["john@example.com"], "age": [30]}
    )
    pii_fields = ["name", "email"]
    df_obfuscated = obfuscate_pii(df.copy(), pii_fields)
    assert (df_obfuscated["name"] == "***").all()  # nosec
    assert (df_obfuscated["email"] == "***").all()  # nosec
    assert (df_obfuscated["age"] == [30]).all()  # nosec


@patch("gdpr_obfuscator.obfuscator.boto3.client")
def test_load_file_from_s3_csv(mock_boto_client):
    sample_csv = "name,email\nJohn Doe,john@example.com\n"
    sample_csv_bytes = sample_csv.encode("utf-8")

    mock_s3 = MagicMock()
    mock_s3.get_object.return_value = {"Body": BytesIO(sample_csv_bytes)}
    mock_boto_client.return_value = mock_s3

    df = load_file_from_s3("s3://test-bucket/test.csv")
    assert not df.empty  # nosec
    assert list(df.columns) == ["name", "email"]  # nosec
    assert df.iloc[0]["name"] == "John Doe"  # nosec


@patch("gdpr_obfuscator.obfuscator.boto3.client")
def test_load_file_from_s3_json(mock_boto_client):
    sample_json = '[{"name": "John Doe", "email": "john@example.com"}]'
    sample_json_bytes = sample_json.encode("utf-8")

    mock_s3 = MagicMock()
    mock_s3.get_object.return_value = {"Body": BytesIO(sample_json_bytes)}
    mock_boto_client.return_value = mock_s3

    df = load_file_from_s3("s3://test-bucket/test.json")
    assert not df.empty  # nosec
    assert list(df.columns) == ["name", "email"]  # nosec
    assert df.iloc[0]["name"] == "John Doe"  # nosec


@patch("gdpr_obfuscator.obfuscator.boto3.client")
def test_load_file_from_s3_parquet(mock_boto_client):
    # Create a sample DataFrame and convert it to Parquet bytes
    df_original = pd.DataFrame({"name": ["John Doe"], "email": ["john@example.com"]})
    buffer = BytesIO()
    df_original.to_parquet(buffer, index=False)
    parquet_bytes = buffer.getvalue()

    mock_s3 = MagicMock()
    mock_s3.get_object.return_value = {"Body": BytesIO(parquet_bytes)}
    mock_boto_client.return_value = mock_s3

    df = load_file_from_s3("s3://test-bucket/test.parquet")
    pd.testing.assert_frame_equal(df, df_original)


@patch("gdpr_obfuscator.obfuscator.boto3.client")
def test_save_file_to_s3_csv(mock_boto_client):
    df = pd.DataFrame({"name": ["John Doe"], "email": ["john@example.com"]})
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3

    output_path = "s3://test-bucket/output.csv"
    save_file_to_s3(df, output_path)

    mock_s3.put_object.assert_called_once()
    args, kwargs = mock_s3.put_object.call_args
    bucket, key = output_path.replace("s3://", "").split("/", 1)
    assert kwargs["Bucket"] == bucket  # nosec
    assert key in kwargs["Key"]  # nosec
    body = kwargs["Body"].decode("utf-8")
    assert "John Doe" in body  # nosec


@patch("gdpr_obfuscator.obfuscator.boto3.client")
def test_save_file_to_s3_json(mock_boto_client):
    df = pd.DataFrame({"name": ["John Doe"], "email": ["john@example.com"]})
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3

    output_path = "s3://test-bucket/output.json"
    save_file_to_s3(df, output_path)

    mock_s3.put_object.assert_called_once()
    args, kwargs = mock_s3.put_object.call_args
    body = kwargs["Body"].decode("utf-8")
    assert "John Doe" in body  # nosec


@patch("gdpr_obfuscator.obfuscator.boto3.client")
def test_save_file_to_s3_parquet(mock_boto_client):
    df = pd.DataFrame({"name": ["John Doe"], "email": ["john@example.com"]})
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3

    output_path = "s3://test-bucket/output.parquet"
    save_file_to_s3(df, output_path)

    mock_s3.put_object.assert_called_once()
    args, kwargs = mock_s3.put_object.call_args
    body = kwargs["Body"]
    buffer = BytesIO(body)
    df_saved = pd.read_parquet(buffer)
    pd.testing.assert_frame_equal(df_saved, df)


@patch("gdpr_obfuscator.obfuscator.save_file_to_s3")
@patch("gdpr_obfuscator.obfuscator.load_file_from_s3")
def test_process_file(mock_load, mock_save):
    df = pd.DataFrame(
        {"name": ["John Doe"], "email": ["john@example.com"], "age": [30]}
    )
    mock_load.return_value = df
    process_file(
        "s3://test-bucket/input.csv", ["name", "email"], "s3://test-bucket/output.csv"
    )
    df_expected = df.copy()
    df_expected[["name", "email"]] = "***"
    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    pd.testing.assert_frame_equal(args[0], df_expected)
