"""
config package

This makes the import shorter, so in main.py I can write:
    from config import DATA_PATH, COLS_TO_DROP
instead of:
    from config.config import DATA_PATH, COLS_TO_DROP
"""

from .config import BASE_DIR, DATA_PATH, COLS_TO_DROP, CATEGORY_LIMIT
