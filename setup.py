from setuptools import setup, find_packages

setup(
    name="gdpr_obfuscator",
    version="1.0.0",
    author="Zabihullah Habibi",
    author_email="your.email@example.com",
    description="A Python library to anonymize personally identifiable information (PII) in CSV files stored in AWS S3.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ZabihullahHabibi/grad-post-programme-projects", 
    packages=find_packages(),
    install_requires=[
        "boto3",
        "pandas"
    ],
    extras_require={
        "dev": ["pytest", "pytest-mock"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
