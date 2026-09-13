from dotenv import load_dotenv

load_dotenv()

import asyncio
import json

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

        requests = db.execute(
            """
            SELECT user_id, request_date
            FROM requests
            ORDER BY request_id
            LIMIT 25
            """
        ).fetchall()

        if len(requests) < 25:
            raise ValueError(
                f"Expected at least 25 requests, found {len(requests)}"
            )


        for request in requests[1:25]:
            world_model = asyncio.run(
                replay(
                    db=db,
                    user_id=request["user_id"],
                    request_date=request["request_date"],
                )
            )

        print(
            f"\nWorld model built for user {request['user_id']}"
        )
        print(json.dumps(world_model, indent=2, default=str))
    
    finally:
        db.close()


if __name__ == "__main__":
    main()