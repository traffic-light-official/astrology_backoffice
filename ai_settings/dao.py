from django.db import connection


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
