import os
import time

import psycopg2
from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor

app = Flask (__name__)

# Configuracion de comunicacon con PostgreSQL
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "tareas_db"),
    "database": os.getenv("DB_NAME", "tareas_db"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "admin123"),
    "port": os.getenv("DB_PORT", "5432"),
}


def get_connection():
    """Establece la conexión con PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)


def initialize_database():
    """Crea la tabla de tareas si todavía no existe."""
    for attempt in range(10):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(150) NOT NULL,
                    description TEXT,
                    completed BOOLEAN DEFAULT FALSE
                );
            """)

            connection.commit()
            cursor.close()
            connection.close()

            print("Base de datos inicializada correctamente.")
            return

        except psycopg2.OperationalError:
            print("Esperando a PostgreSQL...")
            time.sleep(3)

    raise RuntimeError("No fue posible conectar con PostgreSQL.")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "API de registro de tareas funcionando",
        "status": "success"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}

    title = data.get("title")
    description = data.get("description", "")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "El título es obligatorio"}), 400

    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        INSERT INTO tasks (title, description)
        VALUES (%s, %s)
        RETURNING id, title, description, completed;
    """, (title.strip(), description))

    task = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify(task), 201


@app.route("/tasks", methods=["GET"])
def get_tasks():
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id, title, description, completed
        FROM tasks
        ORDER BY id;
    """)

    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(tasks)

print("El archivo app.py se esta ejecutando", flush=True)
print("Valor de name:", __name__, flush=True)

if __name__ == "__main__":
    print("Entramos al bloque pincipal", flush=True)
    initialize_database()
    print("Iniciando servidor Flask", flush=True)
    app.run(host="0.0.0.0", port=5000)