import psycopg2

from settings import db_parameters_string


def get_operators() -> list:
    with psycopg2.connect(db_parameters_string) as conn:
        cur = conn.cursor()
        query = 'SELECT tg_id FROM operators'
        cur.execute(query)
        operators = [int(i[0]) for i in cur.fetchall()]
        return operators
