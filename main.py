import argparse
from gdpr_obfuscator.obfuscator import process_csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GDPR Obfuscator CLI")
    parser.add_argument("file_to_obfuscate", type=str, help="S3 path of the file to obfuscate")
    parser.add_argument("pii_fields", nargs="+", help="Fields to obfuscate")

    args = parser.parse_args()
    output_s3_path = args.file_to_obfuscate.replace(".csv", "_obfuscated.csv")

    process_csv(args.file_to_obfuscate, args.pii_fields, output_s3_path)
    print(f"Obfuscated file saved to {output_s3_path}")
