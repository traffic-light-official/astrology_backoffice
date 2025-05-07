from django.db import connection
from transactions.schemas import TransactionInfo


def get_search_for_users(query: str):
    params = []

    sql_query = ("SELECT * FROM user_info WHERE user_name LIKE %s OR "
             "user_id LIKE %s ORDER BY user_id ASC")

    query = query.strip()
    like_query = f"%{query}%"
    params.extend([like_query, like_query])
    with connection.cursor() as cursor:
        cursor.execute(sql_query, params)
        rows = cursor.fetchall()
    return rows


def get_users():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_info")
        rows = cursor.fetchall()
    return rows


def get_dictionary_user_info(user_id: int):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT user_name, birth_date, birth_time, place_of_birth, zodiac_sign,"
                       f" chinese_zodiac_sign, gender, language FROM user_info WHERE user_id = {user_id}")
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def get_user_activity(user_id: int):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT engagement_level, last_active_date, preferred_communication, notification_opt_in"
                       f" FROM user_activity WHERE user_id = {user_id}")
        row = cursor.fetchone()
    return row


def get_additional_data(user_id: int):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT user_timezone, lunar_phase_preference, retrograde_warning, preferred_astrology_type"
                       f" FROM user_additional_data WHERE user_id = {user_id}")
        row = cursor.fetchone()
    return row


def get_user_interest(user_id: int):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT interest_love, interest_career, interest_money, interest_health, interest_family, "
                       f"interest_travel, interest_spirituality, interest_self_development, interest_daily_horoscope, "
                       f"interest_compatibility FROM user_interest WHERE user_id = {user_id}")
        row = cursor.fetchone()
    return row


def get_user_last_request(user_id: int):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT last_topic, last_question, last_advice_given "
                       f"FROM user_last_request WHERE user_id = {user_id}")
        row = cursor.fetchone()
    return row


def get_user_dialogs(user_id: int):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id, user_id, `role`, content FROM user_dialogs WHERE user_id = {user_id}")
        row = cursor.fetchall()
    return row


def get_dictionary_user_dialog(dialog_id: int):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id, `role`, content FROM user_dialogs WHERE id = {dialog_id}")
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def update_user_info(values: dict, user_id: int):
    query = 'UPDATE user_info SET {}'.format(', '.join('{}=%s'.format(k) for k in values))
    query += f' WHERE user_id = {user_id}'
    with connection.cursor() as cursor:
        cursor.execute(query, values.values())


def update_dialog(values: dict, dialog_id: int):
    query = 'UPDATE user_dialogs SET {}'.format(', '.join('{}=%s'.format(k) for k in values))
    query += f' WHERE id = {dialog_id}'
    with connection.cursor() as cursor:
        cursor.execute(query, values.values())


def remove_dialog(dialog_id: int):
    query = f'DELETE from user_dialogs WHERE id = {dialog_id}'
    with connection.cursor() as cursor:
        cursor.execute(query)


def remove_user(user_id: int):
    query = f'DELETE from user_info WHERE user_id = {user_id}'
    with connection.cursor() as cursor:
        cursor.execute(query)


def get_prompts():
    query = f'SELECT id, system_prompt, soft_prompt FROM prompts'
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
    return row


def get_dictionary_prompts():
    query = f'SELECT system_prompt, soft_prompt FROM prompts'
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def update_prompts(values: dict, prompts_id: int):
    query = 'UPDATE prompts SET {}'.format(', '.join('{}=%s'.format(k) for k in values))
    query += f' WHERE id = {prompts_id}'
    with connection.cursor() as cursor:
        cursor.execute(query, values.values())
