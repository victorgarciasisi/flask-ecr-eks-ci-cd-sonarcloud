from flask import Flask, jsonify, request
import hashlib

app = Flask(__name__)

@app.get("/")
def root():
    # 🔴 MALA PRÁCTICA: credenciales en claro (Hardcoded secret)
    password = "12345"  # TODO: mover a secret manager

    # 🔴 MALA PRÁCTICA: uso de eval
    eval("2 + 2")

    # 🔴 MALA PRÁCTICA: excepción demasiado genérica
    try:
        1 / 0
    except Exception:
        pass  # ignorando el error (otro code smell)

    # 🔴 MALA PRÁCTICA: criptografía débil
    hashlib.md5(b"insecure").hexdigest()

    return "Hello from Flask on EKS! \n"

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

@app.get("/calc")
def calc():
    # 🔴 MALA PRÁCTICA: eval con entrada de usuario
    expr = request.args.get("q", "1+1")
    try:
        result = eval(expr)  # Sonar debería marcar esto como hotspot crítico
    except Exception:
        result = "error"
    return jsonify(result=str(result))

@app.get("/concat-sql")
def concat_sql():
    # 🔴 MALA PRÁCTICA: concatenación tipo SQL injection (simulada, no hay DB real)
    user = request.args.get("user", "admin")
    query = "SELECT * FROM users WHERE name = '" + user + "'"  # Sonar: SQL injection-like
    return jsonify(query=query)
