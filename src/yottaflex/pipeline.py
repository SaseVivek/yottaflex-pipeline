
from __future__ import annotations

import logging
import subprocess
import sys

from .database import connect, load_csv_tables
from .transform import build_analytics_tables


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("Starting YottaFlex data pipeline")

    # Step 1: Load CSV files into staging tables
    logger.info("Loading source CSV files")

    con = connect()

    try:
        counts = load_csv_tables(con)
        logger.info("Staging completed: %s", counts)
    finally:
        con.close()

    # Step 2: Execute data quality checks
    logger.info("Running data quality checks")

    subprocess.run(
        [sys.executable, "-m", "src.yottaflex.quality"],
        check=True
    )

    # Step 3: Build analytics tables
    logger.info("Building analytics tables")

    con = connect()

    try:
        tables = build_analytics_tables(con)
        logger.info(
            "Analytics tables created: %s",
            tables["name"].tolist()
        )
    finally:
        con.close()

    logger.info("YottaFlex pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()
