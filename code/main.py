from dotenv import load_dotenv

load_dotenv()

import asyncio

from pathlib import Path

from data.db import Database
from data.loader.load_all import load_all

from world_model.replay import replay

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

        first_request = db.execute(
            """
            SELECT user_id, request_date
            FROM requests
            WHERE user_id = 'user_02'
            """
        ).fetchone()

        if first_request is None:
            raise ValueError("No requests found in database")

        world_model = asyncio.run(replay(
            db=db,
            user_id=first_request["user_id"],
            request_date=first_request["request_date"],
        ))

        print(
            f"World model built for user {first_request['user_id']}"
        )
        print(world_model)

    finally:
        db.close()


if __name__ == "__main__":
    main()