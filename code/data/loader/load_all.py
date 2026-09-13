from pathlib import Path

from data.db import Database
from .financial_profiles import load_financial_profiles
from .financial_events import load_financial_events
from .exchange_rates import load_exchange_rates
from .requests import load_requests
from .payment_options import load_payment_options
from .images import load_images
from .messages import load_messages


def load_all(db: Database, dataset_dir: str | Path):
    dataset_dir = Path(dataset_dir)

    load_financial_profiles(db, dataset_dir)
    load_financial_events(db, dataset_dir)
    load_exchange_rates(db, dataset_dir)
    load_requests(db, dataset_dir)
    load_payment_options(db, dataset_dir)
    load_images(db, dataset_dir)
    load_messages(db, dataset_dir)

    db.commit()