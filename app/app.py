from flask import Flask, request
import os
import sqlite3

app = Flask(__name__)

# Contraseñas hardcodeadas - VULNERABILIDAD 1
DB_PASSWORD = "supersecreto123"
SECRET_KEY = "clave-super-secreta-hardcodeada"

@app.route('/')
def index():
    return "Hola, soy una app insegura!"

# VULNERABILIDAD 2 - SQL Injection
@app.route('/usuario')
def get_usuario():
    nombre = request.args.get('nombre')
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre = '" + nombre + "'")
    return str(cursor.fetchall())

# VULNERABILIDAD 3 - Command Injection
@app.route('/ping')
def ping():
    host = request.args.get('host')
    resultado = os.system("ping -c 1 " + host)
    return "Resultado: " + str(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
