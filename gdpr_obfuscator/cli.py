import argparse
import os
from gdpr_obfuscator.obfuscator import process_file


def main():
    parser = argparse.ArgumentParser(description="GDPR Obfuscator CLI Tool")
    parser.add_argument(
        "--input_s3",
        required=True,
        help="S3 URI of the input file (CSV, JSON, or Parquet)")
    parser.add_argument(
        "--fields",
        nargs="+",
        required=True,
        help="List of PII fields to obfuscate")
    parser.add_argument(
        "--output_s3",
        help="S3 URI for the obfuscated output file (optional)")
    args = parser.parse_args()

    # Generate output URI if not provided, preserving file extension.
    if args.output_s3:
        output_s3 = args.output_s3
    else:
        base, ext = os.path.splitext(args.input_s3)
        output_s3 = f"{base}_obfuscated{ext}"

    process_file(args.input_s3, args.fields, output_s3)
    print(f"Obfuscated file saved to: {output_s3}")


if __name__ == "__main__":
    main()
