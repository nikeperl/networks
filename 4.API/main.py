from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

import parser


app = Flask(__name__)

# конфиг базы данных
conn = psycopg2.connect(
    dbname="news_db",
    port="5432"
)

def save_to_db(news_list):
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE news RESTART IDENTITY;")

    for data in news_list:
        cursor.execute("""
            INSERT INTO news (title, description, date, author, link) 
            VALUES (%s, %s, %s, %s, %s)
        """, (data["title"], data["description"], data["date"], data["author"], data["link"]))

    conn.commit()
    cursor.close()
    conn.close()

@app.route("/parse", methods=["GET"])
def parse():
    url = request.args.get("url")
    time_limit = request.args.get("time")

    result = parser.parse_website(url, time_limit)
    save_to_db(result)
    return jsonify(result)

@app.route("/data", methods=["GET"])
def get_data():
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM news")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run()
    # http://127.0.0.1:5000/parse?url=https://rozetked.me/news&time=11.03
    # http://127.0.0.1:5000/date
