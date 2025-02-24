import json
from gdpr_obfuscator.obfuscator import process_csv

def lambda_handler(event, context):
    file_to_obfuscate = event["file_to_obfuscate"]
    pii_fields = event["pii_fields"]
    output_s3_path = file_to_obfuscate.replace(".csv", "_obfuscated.csv")

    process_csv(file_to_obfuscate, pii_fields, output_s3_path)
    
    return {"status": "success", "output_file": output_s3_path}
