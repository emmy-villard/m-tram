from datetime import datetime

def get_earliest_date_in_db() -> datetime:
    earliest_date_in_db = datetime(
        year= 2026, month=8, day=26,
        hour=0, minute=0, second=0, microsecond=0
    ) #TODO request to get earliest date from all tables
    return earliest_date_in_db