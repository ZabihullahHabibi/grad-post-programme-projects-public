import argparse
from gdpr_obfuscator.obfuscator import process_csv


def main():
    parser = argparse.ArgumentParser(description="GDPR Obfuscator CLI Tool")
    parser.add_argument(
        "--input_s3", required=True, help="S3 path of the input CSV file"
    )
    parser.add_argument(
        "--fields",
        nargs="+",
        required=True,
        help="List of PII fields to obfuscate")
    parser.add_argument(
        "--output_s3",
        required=True,
        help="S3 path for the obfuscated CSV file")

    args = parser.parse_args()

    process_csv(args.input_s3, args.fields, args.output_s3)
    print(f"Obfuscated file saved to {args.output_s3}")


if __name__ == "__main__":
    main()
