from django.db import connection
from .schemas import TransactionInfo


def create_transactions(values: TransactionInfo):
    parameters_transaction = {
        'id': values.id,
        'user_id': values.client_reference_id,
        'created': values.created,
        'currency': values.currency,
        'presentment_amount': values.presentment_amount,
        'presentment_currency': values.presentment_currency,
        'payment_status': values.payment_status,
        'amount_total': values.amount_total,
        'quantity': values.quantity,
        'payments_account': 'STRIPE'
    }
    query = ('INSERT INTO transactions VALUES (%(id)s, %(user_id)s, %(created)s, %(currency)s, %(presentment_amount)s, '
             '%(presentment_currency)s, %(payment_status)s, %(amount_total)s, %(quantity)s, %(payments_account)s)')
    with connection.cursor() as cursor:
        cursor.execute(query, parameters_transaction)


def get_transactions():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM transactions")
        rows = cursor.fetchall()
    return rows


def get_transactions_by_id(trans_id: str):
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM transactions WHERE id = "{trans_id}"')
        row = cursor.fetchone()
    return row


def get_search_for_transactions(query: str):
    params = []

    sql_query = ("SELECT user_id, created, payment_status, amount_total, currency FROM transactions "
                 "WHERE user_id LIKE %s ORDER BY user_id ASC")

    query = query.strip()
    like_query = f"%{query}%"
    params.extend([like_query])
    with connection.cursor() as cursor:
        cursor.execute(sql_query, params)
        rows = cursor.fetchall()
    return rows


def get_user_astrals(user_id: int):
    query = f'SELECT astrals FROM user_astrals WHERE user_id = {user_id}'
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
    return row[0]


def get_id_transaction(transaction_id: str):
    query = f'SELECT id FROM transactions WHERE id = "{transaction_id}"'
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
    return row


def update_astrals(values: dict, user_id: int):
    query = 'UPDATE user_astrals SET {}'.format(', '.join('{}=%s'.format(k) for k in values))
    query += f' WHERE user_id = {user_id}'
    with connection.cursor() as cursor:
        cursor.execute(query, values.values())
