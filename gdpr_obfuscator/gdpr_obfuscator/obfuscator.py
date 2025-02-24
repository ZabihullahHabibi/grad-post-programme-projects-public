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


# def load_csv_from_s3(s3_path: str, endpoint_url: str = None) -> pd.DataFrame:
#     """
#     Load a CSV file from an S3 bucket into a pandas DataFrame.

#     :param s3_path: S3 URI (e.g., "s3://bucket/key")
#     :param endpoint_url: Optional custom endpoint URL (useful for LocalStack)
#     :return: DataFrame loaded from CSV
#     """
#     client = (
#         boto3.client("s3", endpoint_url=endpoint_url)
#         if endpoint_url
#         else boto3.client("s3")
#     )
#     bucket, key = s3_path.replace("s3://", "").split("/", 1)
#     response = client.get_object(Bucket=bucket, Key=key)
#     data = response["Body"].read()
#     if isinstance(data, bytes):
#         data = data.decode("utf-8")
#     return pd.read_csv(StringIO(data))


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


# def save_csv_to_s3(
#         data: pd.DataFrame, output_s3_path: str, endpoint_url: str = None):
#     """
#     Save a pandas DataFrame as a CSV file to an S3 bucket.

#     :param data: DataFrame to be saved
#     :param output_s3_path: Destination S3 URI (e.g., "s3://bucket/key")
#     :param endpoint_url: Optional custom endpoint URL (useful for LocalStack)
#     """
#     client = (
#         boto3.client("s3", endpoint_url=endpoint_url)
#         if endpoint_url
#         else boto3.client("s3")
#     )
#     bucket, key = output_s3_path.replace("s3://", "").split("/", 1)
#     csv_buffer = StringIO()
#     data.to_csv(csv_buffer, index=False)
#     client.put_object(
#         Bucket=bucket, Key=key, Body=csv_buffer.getvalue().encode("utf-8")
#     )


# def process_csv(
#     file_to_obfuscate: str,
#     pii_fields: list,
#     output_s3_path: str,
#     endpoint_url: str = None,
# ):
#     """
#     Load a CSV file from S3, obfuscate designated PII fields,
#     and save the file back to S3.

#     :param file_to_obfuscate: Source S3 CSV URI
#     :param pii_fields: List of columns to obfuscate
#     :param output_s3_path: Destination S3 CSV URI
#     :param endpoint_url: Optional custom endpoint URL (useful for LocalStack)
#     """
#     df = load_csv_from_s3(file_to_obfuscate, endpoint_url=endpoint_url)
#     df_obfuscated = obfuscate_pii(df, pii_fields)
#     save_csv_to_s3(df_obfuscated, output_s3_path, endpoint_url=endpoint_url)


def process_file(
        file_to_obfuscate: str,
        pii_fields: list,
        output_s3_path: str):
    """
    Load a file from S3, obfuscate PII fields,
    and save it back in the same format.
    """
    df = load_file_from_s3(file_to_obfuscate)
    df_obfuscated = obfuscate_pii(df, pii_fields)
    save_file_to_s3(df_obfuscated, output_s3_path)
