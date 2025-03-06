from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

import subprocess


app = Flask(__name__)

# Подключение к БД
DB_CONFIG = {
    "dbname": "news_db",
    "user": "user",
    "password": "password",
    "host": "db",
    "port": 5432
}

@app.route("/parse", methods=["GET"])
def parse():
    """Запускает парсер с переданным URL"""
    url = request.args.get("url")
    if not url:
        return jsonify({"status": "error", "message": "URL не указан"}), 400

    try:
        result = subprocess.run(["python3", "parser.py", url], capture_output=True, text=True)
        return jsonify({"status": "success", "output": result.stdout})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/data", methods=["GET"])
def get_data():
    """Получает данные из БД и возвращает в JSON"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM news")
        data = cursor.fetchall()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
