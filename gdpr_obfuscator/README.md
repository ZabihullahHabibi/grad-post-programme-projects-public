# GDPR Obfuscator

## Overview

The GDPR Obfuscator is a Python library designed to anonymize personally identifiable information (PII) in CSV files stored in AWS S3. It replaces specified sensitive fields with obfuscated strings (e.g., "***"), ensuring compliance with GDPR requirements for data anonymization.

## Features

- **CSV Processing:** Loads CSV data from an S3 bucket, replaces designated PII fields, and saves the result back to S3.
- **Extensibility:** Built to be extended for additional file formats (JSON, Parquet) in the future.
- **AWS Integration:** Suitable for use with AWS Lambda, EC2, ECS, or other AWS services.
- **Local Testing:** Use CLI for local testing and integrate with LocalStack/moto for AWS simulation.
- **Unit Tested:** Fully unit tested with `pytest` and mocks for AWS services.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/ZabihullahHabibi/grad-post-programme-projects.git
cd grad-post-programme-projects
pip install -r requirements.txt
