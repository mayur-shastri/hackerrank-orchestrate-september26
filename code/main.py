from pathlib import Path

from data.db import Database
from data.loader.load_all import load_all


def main():
    code_dir = Path(__file__).resolve().parent
    project_dir = code_dir.parent

    dataset_dir = project_dir / "dataset"
    db_path = code_dir / "buy_or_wait.db"

    db = Database(db_path)

    try:
        db.initialize()
        load_all(db, dataset_dir)
        print(f"Database initialized successfully: {db_path}")
    finally:
        db.close()


if __name__ == "__main__":
    main()