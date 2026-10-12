"""
MediConnect HMS — Database Package
Exposes connection helper and database initializer.
"""

from db.connection import get_db
from db.schema import init_tables
from db.seed import seed_data_if_empty


def init_db():
    """Initializes schema and seeds baseline records if needed."""
    conn = get_db()
    init_tables(conn)
    seed_data_if_empty(conn)
    conn.close()


__all__ = ["get_db", "init_db"]
