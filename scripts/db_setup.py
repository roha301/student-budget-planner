"""Simple helper to execute SQL files in db/plsql using cx_Oracle"""
import os
import glob
import cx_Oracle

ORACLE_USER = os.environ.get('ORACLE_USER', 'system')
ORACLE_PASSWORD = os.environ.get('ORACLE_PASSWORD', 'oracle')
ORACLE_DSN = os.environ.get('ORACLE_DSN', '//localhost:1521/XE')

SQL_DIR = os.path.join(os.path.dirname(__file__), '..', 'db', 'plsql')


def run_sql_file(connection, path):
    with open(path, 'r', encoding='utf-8') as fh:
        sql = fh.read()
    cursor = connection.cursor()
    try:
        for stmt in sql.split('/\n'):
            stmt = stmt.strip()
            if not stmt:
                continue
            cursor.execute(stmt)
        connection.commit()
    except Exception as e:
        print(f"Error executing {path}: {e}")
        raise


if __name__ == '__main__':
    dsn = ORACLE_DSN
    print('Connecting to', dsn)
    conn = cx_Oracle.connect(ORACLE_USER, ORACLE_PASSWORD, dsn)
    sql_files = sorted(glob.glob(os.path.join(SQL_DIR, '*.sql')))
    for f in sql_files:
        print('Running', f)
        run_sql_file(conn, f)
    conn.close()
    print('Done.')
