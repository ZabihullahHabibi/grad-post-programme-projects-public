# lambda_function.py

import json
from gdpr_obfuscator.obfuscator import process_csv

def lambda_handler(event, context):
    """
    AWS Lambda handler that processes an event containing:
      - file_to_obfuscate: S3 URI of the CSV file
      - pii_fields: List of fields to obfuscate
    It creates an output file by replacing '.csv' with '_obfuscated.csv' in the source path.
    """
    file_to_obfuscate = event["file_to_obfuscate"]
    pii_fields = event["pii_fields"]
    output_s3_path = file_to_obfuscate.replace(".csv", "_obfuscated.csv")
    
    process_csv(file_to_obfuscate, pii_fields, output_s3_path)
    
    return {"status": "success", "output_file": output_s3_path}
