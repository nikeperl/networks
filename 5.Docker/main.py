from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# конфиг базы данных
database_url = "postgresql://myuser:qwerty@postgres:5432/urlsdb"

def execute_db_query(query, params=None, fetch=False):
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())

        if fetch:
            return cursor.fetchall()
        else:
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


@app.route("/save", methods=["GET"])
def save():
    try:
        url = request.args.get("url")
        execute_db_query("INSERT INTO urls (url) VALUES (%s)", (url,))
        return f"New url in table: {url}"
    except Exception as e:
        return f"Error saving url: {e}"


@app.route("/data", methods=["GET"])
def get_data():
    try:
        data = execute_db_query("SELECT * FROM urls", fetch=True)
        return jsonify(data)
    except Exception as e:
        return f"Error retrieving data: {e}"


@app.route("/clear")
def clear():
    try:
        execute_db_query("DELETE FROM urls")
        execute_db_query("ALTER SEQUENCE urls_id_seq RESTART WITH 1")
        return "Table 'urls' cleared successfully!"
    except Exception as e:
        return f"Error clearing table: {e}"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    # http://127.0.0.1:5000/save?url=https://rozetked.me/news
    # http://127.0.0.1:5000/data
    # http://127.0.0.1:5000/clear
