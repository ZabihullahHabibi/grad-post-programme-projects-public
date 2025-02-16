import boto3
import pandas as pd
from io import StringIO

def load_csv_from_s3(s3_path: str):
    """Load a CSV file from an S3 bucket into a pandas DataFrame."""
    s3 = boto3.client("s3")
    bucket, key = s3_path.replace("s3://", "").split("/", 1)

    response = s3.get_object(Bucket=bucket, Key=key)
    data = response["Body"].read()

    if isinstance(data, bytes):  # Decode only if it's bytes
        data = data.decode("utf-8")

    return pd.read_csv(StringIO(data))


def obfuscate_pii(data: pd.DataFrame, pii_fields: list):
    """Replace specified PII fields with '***'."""
    data[pii_fields] = "***"
    return data