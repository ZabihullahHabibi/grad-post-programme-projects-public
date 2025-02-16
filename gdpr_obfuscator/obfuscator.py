import boto3
import pandas as pd
from io import StringIO

def load_csv_from_s3(s3_path: str):
    """Load a CSV file from an S3 bucket into a pandas DataFrame."""
    s3 = boto3.client("s3")
    bucket, key = s3_path.replace("s3://", "").split("/", 1)

    response = s3.get_object(Bucket=bucket, Key=key)
    data = response["Body"].read().decode("utf-8")

    return pd.read_csv(StringIO(data))
