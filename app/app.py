from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    "host": "db",
    "database": "mydatabase",
    "user": "user",
    "password": "password"
}

@app.route('/')
def home():
    return "Hello, World!!"

@app.route('/data')
def get_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50)
            )
        """)
        conn.commit()

        for i in range(50):
            cursor.execute("INSERT INTO test_table (name) VALUES (%s)", ("Юрков Максим БСБО-02-23",))
        conn.commit()

        cursor.execute("SELECT * FROM test_table")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rows)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
