from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
QUARANTINE_DIR = DATA_DIR / "quarantine"
REPORTS_DIR = ROOT / "reports"
LOGS_DIR = ROOT / "logs"
DB_PATH = DATA_DIR / "yottaflex.duckdb"

TABLES = ("customers", "products", "orders", "order_items", "payments")
