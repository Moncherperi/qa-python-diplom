import pymysql

# Устанавливаем соединение с базой данных MySQL в Docker (внешний порт 3307)
def get_connection():
    host = 'localhost'
    port = 3307
    user = 'app'
    password = 'pass'
    database = 'app'

    return pymysql.connect(host=host, port=port, user=user, password=password, database=database)

# Очищаем все рабочие таблицы перед запуском каждого нового теста
def clear_tables():
    connection = get_connection()
    # Создаём курсор для выполнения SQL-запросов
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM payment_entity;")
        cursor.execute("DELETE FROM credit_request_entity;")
        cursor.execute("DELETE FROM order_entity;")
    # Сохраняем изменения в базе и закрываем соединение
    connection.commit()
    connection.close()

# Получаем статус (APPROVED или DECLINED) самой последней записи из нужной таблицы
def get_status(table_name):
    connection = get_connection()
    with connection.cursor() as cursor:
        # Сортируем записи по времени создания от новых к старым и берём 1 последнюю
        cursor.execute(f"SELECT status FROM {table_name} ORDER BY created DESC LIMIT 1;")
        status = cursor.fetchone()
        connection.close()
        # Возвращаем сам текст статуса из кортежа или None, если таблица пустая
        if status is not None:
            return status[0]
        else:
            return None
