from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc
import logging

app = Flask(__name__)

# Разрешаем все источники для CORS
CORS(app)

# Строка подключения к базе данных
conn_str = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-0VL516Q\\SQLEXPRESS;"  # Обновите на имя вашего сервера
    "DATABASE=ApplicationDB;"  # Укажите вашу базу данных
    "Trusted_Connection=yes;"  # Использование доверенного подключения
)

# Логирование ошибок
logging.basicConfig(level=logging.DEBUG)

# Функция для вставки заявки в базу данных
def insert_application(user_name, status, tariff):
    try:
        conn = pyodbc.connect(conn_str)
        logging.debug("Соединение с базой данных успешно установлено")
        cursor = conn.cursor()
        logging.debug(f"Вставка данных: Имя = {user_name}, Статус = {status}, Тариф = {tariff}")
        cursor.execute(
            "INSERT INTO Applications (UserName, Status, Tariff) VALUES (?, ?, ?)",
            (user_name, status, tariff)
        )
        conn.commit()
        cursor.close()
        conn.close()
        logging.debug("Данные успешно вставлены в базу данных")
        return True
    except Exception as e:
        logging.error(f"Ошибка при вставке в базу данных: {e}")
        return False

@app.route('/submit_application', methods=['POST'])
def submit_application():
    data = request.json
    if not data or 'user_name' not in data or 'tariff' not in data:
        logging.error("Получены некорректные данные")
        return jsonify({"error": "Invalid data"}), 400  # Возвращаем ошибку при неправильных данных
    
    user_name = data['user_name']
    status = "В ожидании"  # Статус заявки
    tariff = data['tariff']  # Получаем тариф

    logging.debug(f"Получено имя: {user_name}, Статус: {status}, Тариф: {tariff}")

    success = insert_application(user_name, status, tariff)
    if success:
        return jsonify({"message": "Заявка принята"}), 200  # Ответ для клиента
    else:
        logging.error("Ошибка при сохранении заявки")
        return jsonify({"error": "Ошибка при сохранении заявки"}), 500

if __name__ == '__main__':
    app.run(debug=True)
