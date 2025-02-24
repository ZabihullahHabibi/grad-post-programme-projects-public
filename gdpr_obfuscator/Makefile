.PHONY: install lint format test package deploy clean run

# Variables
PROJECT = gdpr_obfuscator
LAMBDA_FUNCTION = lambda_function.py
ZIPFILE = gdpr_obfuscator.zip
LAMBDA_NAME = gdprObfuscator

# Install dependencies and pre-commit hooks
install:
	pip install -r requirements.txt
	pre-commit install

# Run code quality checks: PEP-8 (flake8), security scan (bandit), and formatting check (black)
lint:
	flake8 .
	bandit -r .
	black --check .

# Auto-format the code with Black
format:
	black .

# Run all unit tests with pytest
test:
	pytest --maxfail=1 --disable-warnings -q

# Package the Lambda function code into a zip file
package:
	@echo "Packaging the Lambda function..."
	zip -r $(ZIPFILE) $(PROJECT)/ $(LAMBDA_FUNCTION)

# Deploy the packaged code to AWS Lambda using AWS CLI
deploy: package
	@echo "Deploying $(ZIPFILE) to AWS Lambda..."
	aws lambda update-function-code --function-name $(LAMBDA_NAME) --zip-file fileb://$(ZIPFILE)

# Clean up temporary files and caches
clean:
	@echo "Cleaning up temporary files..."
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -f $(ZIPFILE)


