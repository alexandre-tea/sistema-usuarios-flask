import sqlite3
from flask import (
    Blueprint,
    request, 
    render_template, 
    redirect, 
    url_for, 
    session,
    flash
)
from app.banco import buscar_usuario, cadastrar_usuario
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from app.decorators import login_obrigatorio

auth = Blueprint("auth",__name__)

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        senha = request.form["senha"]
        
        usuario_encontrado = buscar_usuario(usuario)

        if usuario_encontrado:

            if check_password_hash(usuario_encontrado[4], senha):

                session["usuario"] = usuario

                return redirect(url_for("auth.home"))
            
        flash("Usuário ou senha inválidos.")

        return render_template("login.html")

    return render_template("login.html")

@auth.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        senha_hash = generate_password_hash(senha)

        try:
            cadastrar_usuario(nome, email, usuario, senha_hash)

            return redirect(url_for("auth.login"))

        except sqlite3.IntegrityError:

            flash("Usuário ou senha inválidos.")
        
            return render_template("login.html")
        
    return render_template("cadastro.html")
    
@auth.route("/logout")
def logout():

    session.pop("usuario", None)

    return redirect(url_for("auth.login"))

@auth.route("/home")
@login_obrigatorio
def home():
    return render_template(
        "home.html",
        usuario=session["usuario"]
    )