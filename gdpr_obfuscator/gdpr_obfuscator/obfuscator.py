import os
import boto3
import pandas as pd
from io import StringIO, BytesIO


def load_file_from_s3(s3_path: str):
    """
    Load a file from S3 and return a pandas DataFrame.
    Supports CSV, JSON, and Parquet based on the file extension.
    """
    extension = os.path.splitext(s3_path)[-1].lower()
    s3 = boto3.client("s3")
    bucket, key = s3_path.replace("s3://", "").split("/", 1)
    response = s3.get_object(Bucket=bucket, Key=key)
    data = response["Body"].read()

    # For CSV and JSON, data is decoded as UTF-8 text.
    if extension in [".csv", ".json"]:
        data = data.decode("utf-8")
        buffer = StringIO(data)
        if extension == ".csv":
            return pd.read_csv(buffer)
        else:  # .json
            return pd.read_json(buffer)
    elif extension == ".parquet":
        buffer = BytesIO(data)
        return pd.read_parquet(buffer)
    else:
        raise ValueError("Unsupported file format: " + extension)


def obfuscate_pii(data: pd.DataFrame, pii_fields: list) -> pd.DataFrame:
    """
    Replace specified PII fields with '***' in the DataFrame.

    :param data: Input pandas DataFrame
    :param pii_fields: List of columns to obfuscate
    :return: Modified DataFrame with obfuscated PII fields
    """
    data[pii_fields] = "***"
    return data


def save_file_to_s3(data: pd.DataFrame, output_s3_path: str):
    """
    Save a pandas DataFrame to S3 in the same format as indicated by the file
    extension. Supports CSV, JSON, and Parquet.
    """
    extension = os.path.splitext(output_s3_path)[-1].lower()
    s3 = boto3.client("s3")
    bucket, key = output_s3_path.replace("s3://", "").split("/", 1)

    if extension == ".csv":
        buffer = StringIO()
        data.to_csv(buffer, index=False)
        body = buffer.getvalue().encode("utf-8")
    elif extension == ".json":
        buffer = StringIO()
        data.to_json(buffer, orient="records", lines=True)
        body = buffer.getvalue().encode("utf-8")
    elif extension == ".parquet":
        buffer = BytesIO()
        data.to_parquet(buffer, index=False)
        body = buffer.getvalue()
    else:
        raise ValueError("Unsupported file format: " + extension)

    s3.put_object(Bucket=bucket, Key=key, Body=body)


def process_file(file_to_obfuscate: str, pii_fields: list, output_s3_path: str):
    """
    Load a file from S3, obfuscate PII fields,
    and save it back in the same format.
    """
    df = load_file_from_s3(file_to_obfuscate)
    df_obfuscated = obfuscate_pii(df, pii_fields)
    save_file_to_s3(df_obfuscated, output_s3_path)
