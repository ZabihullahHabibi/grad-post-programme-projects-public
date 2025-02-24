# GDPR Obfuscator

This tool anonymizes personally identifiable information (PII) in CSV files stored in AWS S3.

## Features
- Loads CSV files from S3.
- Obfuscates specified PII fields.
- Saves the obfuscated file back to S3.
- Can be run locally via CLI or deployed as an AWS Lambda function.

## Installation
```sh
pip install -r requirements.txt
