"""
Main entry point for the Birthday Harmonizer application.
"""

import logging
from src.config import setup_logging
from src.parser import ICSParser
from src.generator import ICSGenerator

logger = logging.getLogger(__name__)


def main() -> None:
    """
    Execution pipeline: Setup -> Parse -> Harmonize -> Save.
    """
    setup_logging()
    logger.info("Starting Birthday Harmonization process...")

    # 1. Parse existing data
    parser = ICSParser("data/input.ics")
    birthday_data = parser.parse()

    if not birthday_data:
        logger.error("No entries found to process. Exiting.")
        return

    logger.info(f"Successfully parsed {len(birthday_data)} entries.")

    # 2. Generate harmonized ICS
    generator = ICSGenerator()
    clean_ics = generator.build(birthday_data)

    # 3. Write to output
    output_path = "data/output.ics"
    try:
        with open(output_path, "wb") as f:
            f.write(clean_ics)
        logger.info(f"Harmonization complete! Clean file saved to: {output_path}")
    except IOError as e:
        logger.error(f"Failed to write output file: {e}")


if __name__ == "__main__":
    main()
