"""MySQL database configuration for the HRM project."""
import os
from pathlib import Path

# Load .env from the package root (QL_Nhan_Su_Python/.env)  
# From app/database/db_config.py, go up 2 levels to reach QL_Nhan_Su_Python/
env_path = Path(__file__).resolve().parents[2] / ".env"
if env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
    except ImportError:
        # Manual parsing if python-dotenv not available
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                os.environ.setdefault(key, val)

# MySQL connection settings (required)
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER") 
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Validate required MySQL credentials
if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
    missing = [k for k, v in [
        ("DB_HOST", DB_HOST),
        ("DB_USER", DB_USER), 
        ("DB_PASSWORD", DB_PASSWORD),
        ("DB_NAME", DB_NAME)
    ] if not v]
    raise ValueError(f"Missing required MySQL environment variables: {missing}")
