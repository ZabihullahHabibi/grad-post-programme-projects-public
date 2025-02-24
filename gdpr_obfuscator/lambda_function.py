import os
from gdpr_obfuscator.obfuscator import process_file


def lambda_handler(event, context):
    """
    AWS Lambda handler that processes an event containing:
      - file_to_obfuscate: S3 URI of the file (CSV, JSON, or Parquet)
      - pii_fields: List of fields to obfuscate

    The output file is created by appending '_obfuscated'
    before the file extension. For example, if the input
    file is 's3://bucket/data.csv', the output will be
    's3://bucket/data_obfuscated.csv'.
    """
    file_to_obfuscate = event["file_to_obfuscate"]
    pii_fields = event["pii_fields"]

    # Extract base name and extension from the input file
    base, ext = os.path.splitext(file_to_obfuscate)
    output_s3_path = f"{base}_obfuscated{ext}"

    # Process the file using the extended function supporting CSV, JSON, and
    # Parquet.
    process_file(file_to_obfuscate, pii_fields, output_s3_path)

    return {"status": "success", "output_file": output_s3_path}
