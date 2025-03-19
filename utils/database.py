import sqlite3

db_name="settings.db"


def set_variable(user_id, variable_name, variable_value):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Вставляем или обновляем значение переменной
    cursor.execute('''
    INSERT OR REPLACE INTO variables (user_id, variable_name, variable_value)
    VALUES (?, ?, ?)
    ''', (user_id, variable_name, variable_value))

    conn.commit()
    conn.close()
    return variable_value


def get_variable(user_id, variable_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Запрос для получения значения переменной по user_id и variable_name
    cursor.execute('''
    SELECT variable_value FROM variables WHERE user_id = ? AND variable_name = ?
    ''', (user_id, variable_name))

    # Получение результата
    result = cursor.fetchone()
    conn.close()

    # Если значение найдено, возвращаем его, иначе None
    return result[0] if result else None

import sqlite3

db_name = "settings.db"

# Глобальная инструкция, которая будет задана при первом обращении
DEFAULT_INSTRUCTION = ('Ты — помощник, который всегда вежлив и помогает пользователю. Я предоставляю тебе историю нашей '
                       'переписки. Отвечая на вопросы учитывай её. Отвечай на языке, который используется в диалоге. '
                       'Если тебя спросят, кто ты такой, то отвечай, что "Нейро", помощник, созданный @stavrmoris. '
                       'Но только если спросят!')

def create_message_history_table():
    """
    Создает таблицу для хранения истории сообщений.
    Если таблица создается впервые, добавляет инструкцию как первое сообщение.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS message_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        is_instruction BOOLEAN NOT NULL DEFAULT 0,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Проверяем, есть ли уже инструкция в таблице
    cursor.execute('''
    SELECT COUNT(*) FROM message_history WHERE is_instruction = 1
    ''')
    instruction_exists = cursor.fetchone()[0] > 0

    # Если инструкции нет, добавляем её
    if not instruction_exists:
        cursor.execute('''
        INSERT INTO message_history (user_id, message, is_instruction)
        VALUES (?, ?, ?)
        ''', (0, DEFAULT_INSTRUCTION, True))

    conn.commit()
    conn.close()

def add_message(user_id, message):
    """
    Добавляет сообщение в историю переписки для указанного пользователя.
    Если история превышает 5000 символов, удаляет последнее сообщение.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Проверяем общую длину истории сообщений для пользователя
    cursor.execute('''
    SELECT SUM(LENGTH(message)) FROM message_history WHERE user_id = ? AND is_instruction = 0
    ''', (user_id,))
    total_length = cursor.fetchone()[0] or 0

    # Если общая длина превышает 5000 символов, удаляем последнее сообщение
    if total_length + len(message) > 5000:
        cursor.execute('''
        DELETE FROM message_history WHERE id = (
            SELECT id FROM message_history WHERE user_id = ? AND is_instruction = 0 ORDER BY timestamp ASC LIMIT 1
        )
        ''', (user_id,))

    # Добавляем новое сообщение
    cursor.execute('''
    INSERT INTO message_history (user_id, message, is_instruction)
    VALUES (?, ?, ?)
    ''', (user_id, message, False))

    conn.commit()
    conn.close()

def clear_message_history(user_id):
    """
    Очищает историю сообщений для указанного пользователя, кроме инструкции.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
    DELETE FROM message_history WHERE user_id = ? AND is_instruction = 0
    ''', (user_id,))

    conn.commit()
    conn.close()

def get_message_history(user_id):
    """
    Возвращает историю переписки для указанного пользователя, включая инструкцию.
    Инструкция всегда будет первой в списке.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Получаем инструкцию (она всегда одна и с is_instruction = 1)
    cursor.execute('''
    SELECT message FROM message_history WHERE is_instruction = 1
    ''')
    instruction = cursor.fetchone()

    # Получаем историю переписки для пользователя
    cursor.execute('''
    SELECT message FROM message_history WHERE user_id = ? AND is_instruction = 0 ORDER BY timestamp ASC
    ''', (user_id,))
    history = cursor.fetchall()

    conn.close()

    # Возвращаем инструкцию и историю переписки
    return [instruction[0]] + [msg[0] for msg in history] if instruction else [msg[0] for msg in history]

def create_user_list_table():
    """
    Создает таблицу для хранения списка user_id.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_list (
        user_id INTEGER PRIMARY KEY
    )
    ''')

    conn.commit()
    conn.close()

def add_user_to_list(user_id):
    """
    Добавляет user_id в список, если его еще нет в таблице.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Проверяем, есть ли уже user_id в таблице
    cursor.execute('''
    SELECT COUNT(*) FROM user_list WHERE user_id = ?
    ''', (user_id,))
    user_exists = cursor.fetchone()[0] > 0

    # Если user_id нет, добавляем его
    if not user_exists:
        cursor.execute('''
        INSERT INTO user_list (user_id)
        VALUES (?)
        ''', (user_id,))

    conn.commit()
    conn.close()

def get_user_list():
    """
    Возвращает список всех user_id из таблицы user_list.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Получаем все user_id из таблицы
    cursor.execute('''
    SELECT user_id FROM user_list
    ''')
    user_ids = cursor.fetchall()

    conn.close()

    # Возвращаем список user_id, убирая кортежи
    return [user_id[0] for user_id in user_ids]
