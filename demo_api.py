# demo_api.py
# Demonstrates the external API integration by logging
# several sample errors and displaying the results.
#
# Run this to see the UUIDTools API being called live.
# Usage: python3 demo_api.py

from logger import Logger


def demonstrate_api_logging():
    """
    Demonstrates the full API-powered logging workflow.
    Each call to log_error() triggers a live API call
    to https://www.uuidtools.com/api/generate/v1
    """

    print("\n" + "=" * 60)
    print("  EXTERNAL API DEMONSTRATION")
    print("  UUIDTools API — GUID Generation for Error Logging")
    print("=" * 60)

    # Create logger instance
    logger = Logger()

    print("\n--- Logging Error 1 ---")
    logger.log_error(
        filename="medical_data_june_2023.csv",
        reason="Filename does not match required convention"
    )

    print("\n--- Logging Error 2 ---")
    logger.log_error(
        filename="MED_DATA_20230603150200.csv",
        reason="Incorrect headers: 'batch' instead of 'batch_id'"
    )

    print("\n--- Logging Error 3 ---")
    logger.log_error(
        filename="MED_DATA_20230603150400.csv",
        reason="Duplicate batch_id '55' found at row 3"
    )

    print("\n--- Logging Error 4 ---")
    logger.log_error(
        filename="MED_DATA_20230603150500.csv",
        reason="Reading value 10.5 exceeds maximum allowed (9.9)"
    )

    print("\n--- Logging Error 5 ---")
    logger.log_error(
        filename="INVALID_empty_file.csv",
        reason="File is empty (0 bytes)"
    )

    # Display all logged entries
    print("\n--- Displaying Complete Error Log ---")
    logger.display_log()


if __name__ == '__main__':
    demonstrate_api_logging()