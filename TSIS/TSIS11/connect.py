import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG


def get_connection(dict_cursor=False):
    """
    Create a PostgreSQL connection.
    Use dict_cursor=True when rows should be returned as dictionaries.
    """
    cursor_factory = RealDictCursor if dict_cursor else None
    return psycopg2.connect(**DB_CONFIG, cursor_factory=cursor_factory)
