import psycopg2

from settings import db_parameters_string, CLIENT_ID


def check_auth(admin_id: int) -> bool:
    with psycopg2.connect(db_parameters_string) as conn:
        cur = conn.cursor()
        query = 'SELECT exists (SELECT 1 FROM operators ' \
                '               WHERE tg_id = %s LIMIT 1);'
        cur.execute(query, (admin_id,))
        return cur.fetchone()[0]


def get_operator_group(op_id: int) -> str:
    with psycopg2.connect(db_parameters_string) as conn:
        cur = conn.cursor()
        query = 'SELECT op_group FROM operators ' \
                'WHERE tg_id = %s'
        cur.execute(query, (op_id,))
        return cur.fetchone()[0]


def get_client_name(client_id: int) -> str:
    with psycopg2.connect(db_parameters_string) as conn:
        cur = conn.cursor()
        query = 'SELECT client_name FROM clients ' \
                'WHERE tg_id = %s'
        cur.execute(query, (client_id,))
        return cur.fetchone()[0]


def check_operator_access(op_id: int) -> bool:
    with psycopg2.connect(db_parameters_string) as conn:
        cur = conn.cursor()
        worker = get_operator_type(CLIENT_ID)

        query = 'SELECT op_type FROM operators WHERE tg_id = %s'
        cur.execute(query, (op_id,))
        op_type = cur.fetchone()[0]
        return worker == op_type


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
                'WHERE op_type = %s'
        cur.execute(query, (operator_type,))
        operators = [int(i[0]) for i in cur.fetchall()]
        return operators


def get_all_admins() -> list:
    with psycopg2.connect(db_parameters_string) as conn:
        cur = conn.cursor()
        query = 'SELECT tg_id FROM operators ' \
                'WHERE op_type = \'op\''
        cur.execute(query)
        operators = [int(i[0]) for i in cur.fetchall()]
        return operators


def change_worker(client_id: int, worker: str) -> None:
    with psycopg2.connect(db_parameters_string) as conn:
        cur = conn.cursor()
        query = 'UPDATE clients SET worker = %s ' \
                'WHERE tg_id = %s'
        cur.execute(query, (worker, client_id))
        conn.commit()
