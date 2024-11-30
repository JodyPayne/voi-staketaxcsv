import argparse
import datetime
import logging
import os
from voi_exporter import export_data
from staketaxcsv.common.ExporterTypes import FORMAT_DEFAULT, FORMATS
from staketaxcsv.settings_csv import REPORTS_DIR

ALL = "all"
DEBUG_ENV_VAR = "STAKETAX_DEBUG_CACHE"


def main_default():
    """
    Entry point for generating reports.
    """
    logging.basicConfig(level=logging.INFO)
    wallet_address, export_format, options = parse_args()
    run_report(wallet_address, export_format, options)


def run_report(wallet_address, export_format, options):
    """
    Generates reports based on the provided wallet address, export format, and options.
    """
    if options.get("historical"):
        # Placeholder for historical balance processing, if implemented
        print(f"Generating historical balances for wallet {wallet_address}")
    elif export_format == ALL:
        # Generate reports in all available formats
        for fmt in FORMATS:
            generate_csv(wallet_address, fmt, options)
    else:
        # Generate report in the specified format
        generate_csv(wallet_address, export_format, options)


def generate_csv(wallet_address, export_format, options):
    """
    Generates a CSV report for a specific format and wallet address.
    """
    path = os.path.join(REPORTS_DIR, f"{wallet_address}.{export_format}.csv")
    try:
        export_data(export_format, wallet_address)
        print(f"Report generated successfully: {path}")
    except Exception as e:
        logging.error(f"Error generating report for wallet {wallet_address} in format {export_format}: {e}")


def parse_args():
    """
    Parses command-line arguments for the script.
    """
    parser = argparse.ArgumentParser(description="VOI Report Utility")
    parser.add_argument(
        "wallet_address",
        help="Wallet address for which to generate reports",
    )
    parser.add_argument(
        "--format",
        type=str,
        default=FORMAT_DEFAULT,
        choices=[ALL] + FORMATS,
        help="Specify the export format. Use 'all' to generate all formats.",
    )
    parser.add_argument(
        "--historical",
        action="store_true",
        default=False,
        help="Generate historical balances report",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debug mode",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Maximum number of transactions to process",
    )

    args = parser.parse_args()

    options = {}
    if args.historical:
        options["historical"] = args.historical
    if args.debug:
        options["debug"] = True
        logging.basicConfig(level=logging.DEBUG)
    if args.limit:
        options["limit"] = args.limit

    return args.wallet_address, args.format, options


def read_common_options(localconfig, options):
    """
    Updates local configuration with provided options.
    """
    localconfig.job = options.get("job", None)
    localconfig.debug = options.get("debug", False)
    localconfig.limit = options.get("limit", localconfig.limit)
    localconfig.koinlynullmap = options.get("koinlynullmap", localconfig.koinlynullmap)


if __name__ == "__main__":
    main_default()
