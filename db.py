import psycopg2

from settings import db_parameters_string


def get_operator_type(client_id: int) -> str:
    with psycopg2.connect(db_parameters_string) as conn:
        cur = conn.cursor()
        query = 'SELECT worker FROM clients ' \
                'WHERE tg_id = %s'
        cur.execute(query, (client_id,))
        return cur.fetchone()[0]


def get_operators(client_id: int) -> list:
    with psycopg2.connect(db_parameters_string) as conn:
        operator_type = get_operator_type(client_id)
        cur = conn.cursor()
        query = 'SELECT tg_id FROM operators ' \
                'WHERE type = %s'
        cur.execute(query, (operator_type,))
        operators = [int(i[0]) for i in cur.fetchall()]
        return operators


def change_worker(client_id: int, worker: str) -> None:
    with psycopg2.connect(db_parameters_string) as conn:
        cur = conn.cursor()
        query = 'UPDATE clients SET worker = %s ' \
                'WHERE tg_id = %s'
        cur.execute(query, (worker, client_id))
        conn.commit()
