from flask import Flask, request
import sqlite3
import os
import subprocess

app = Flask(__name__)

# ❌ MAL:
# Contraseña escrita directamente en el código
PASSWORD = "123456"

# ✅ CORRECTO:
# Usar variables de entorno
# PASSWORD = os.getenv("PASSWORD")


@app.route('/')
def inicio():
    return "App vulnerable"


# ---------------------------
# VULNERABILIDAD 2 - SQL Injection
# ---------------------------
@app.route('/login')
def login():

    usuario = request.args.get('user')

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # ❌ MAL:
    # El usuario controla parte del SQL
    query = f"SELECT * FROM usuarios WHERE nombre = '{usuario}'"

    cursor.execute(query)

    # ✅ CORRECTO:
    # Separar el SQL de los datos del usuario
    # cursor.execute(
    #     "SELECT * FROM usuarios WHERE nombre = ?",
    #     (usuario,)
    # )

    return str(cursor.fetchall())


# ---------------------------
# VULNERABILIDAD 3 - Command Injection
# ---------------------------
@app.route('/ping')
def ping():

    host = request.args.get('host')

    # ❌ MAL:
    # El usuario controla el comando del sistema
    os.system(f"ping -c 1 {host}")

    # ✅ CORRECTO:
    # Pasar argumentos separados y sin shell
    # subprocess.run(
    #     ["ping", "-c", "1", host],
    #     shell=False
    # )

    return "Ping ejecutado"


# ❌ MAL:
# debug=True muestra errores internos

# ✅ CORRECTO:
# debug=False en producción
app.run(debug=True)