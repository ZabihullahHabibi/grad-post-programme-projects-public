# GDPR Obfuscator

## Overview
The GDPR Obfuscator is a Python library for anonymizing personally identifiable information (PII) in data files stored on AWS S3. It replaces specified sensitive fields with obfuscated strings (e.g., "***") and is designed for integration into AWS workflows (Lambda, EC2, ECS) as well as local development and testing.

## Installation

### 1. Clone the Repository
    git clone https://github.com/ZabihullahHabibi/grad-post-programme-projects-public.git
    cd grad-post-programme-projects-public

### 2. Set Up a Virtual Environment
It is recommended to use a virtual environment for development:

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install Dependencies
    pip install -r requirements.txt

## Usage

### For Developers

#### Running Unit Tests
    pytest -v

#### Code Quality and Security Checks
    make lint       # Runs flake8, bandit, and black --check
    make format     # Auto-formats the code using Black

### Local Development & Testing (CLI)
A CLI tool is provided for local testing:

    python cli.py --input_s3 <S3_URI_of_input_file> --fields name email --output_s3 <S3_URI_for_output_file>

If `--output_s3` is not provided, the tool will automatically generate an output URI by appending `_obfuscated` before the file extension.

### As a Client (Library Integration)

You can install the package and integrate it into your own Python projects:

**Install the Package**:

    pip install .

**Usage Example**:

    from gdpr_obfuscator.obfuscator import process_file

    # Process a CSV file stored on S3
    process_file("s3://your-bucket/input.csv", ["name", "email"], "s3://your-bucket/output_obfuscated.csv")

## AWS Deployment
The repository includes:

- **Lambda Handler**: `lambda_function.py` serves as an AWS Lambda entry point.
- **SAM Template**: `gdpr_obfuscator_template.yaml` contains configuration for deploying the function with AWS SAM.

Refer to the SAM template for detailed deployment instructions.

## Additional Information
- **Virtual Environment**: Ensure you use the provided virtual environment (`venv/`) which is excluded from Git tracking via `.gitignore`.
- **Feedback & Support**: For any issues or questions, please contact the project maintainer.
