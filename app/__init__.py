from flask import Flask, render_template
from app.auth import auth
from app.usuario import usuario
from app.banco import conectar, criar_tabela
from app.config import SECRET_KEY


app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY


app.register_blueprint(auth)
app.register_blueprint(usuario)

@app.route("/")
def inicio():
    return render_template("index.html")


conexao = conectar()
criar_tabela(conexao)
conexao.close()
