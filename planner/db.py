import os

import cx_Oracle

ORACLE_USER = os.environ.get("ORACLE_USER", "system")
ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD", "oracle")
ORACLE_DSN = os.environ.get("ORACLE_DSN", "//localhost:1521/XE")


def get_connection():
    dsn = ORACLE_DSN
    return cx_Oracle.connect(ORACLE_USER, ORACLE_PASSWORD, dsn)


def call_get_monthly_spend(user_id: int, year: int, month: int):
    conn = get_connection()
    cursor = conn.cursor()
    out_cursor = conn.cursor()
    try:
        cursor.callproc(
            "get_monthly_spend", [user_id, year, month, out_cursor]
        )
        rows = out_cursor.fetchall()
        return [{"category": r[0], "total": float(r[1] or 0)} for r in rows]
    finally:
        out_cursor.close()
        cursor.close()
        conn.close()
