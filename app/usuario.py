from flask import (
    Blueprint,
    request, 
    render_template, 
    redirect, 
    url_for, 
    session, 
    flash
)

from app.banco import (
    buscar_usuario,
    atualizar_usuario,
    atualizar_senha,
    excluir_usuario
)

from app.decorators import login_obrigatorio
from werkzeug.security import check_password_hash


usuario = Blueprint("usuario",__name__)

@usuario.route("/perfil", methods=["GET", "POST"])
@login_obrigatorio
def perfil():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]

        atualizar_usuario(
            nome,
            email,
            session["usuario"]
        )

        return redirect(url_for("usuario.perfil"))

    usuario = buscar_usuario(session["usuario"])

    return render_template(
        "perfil.html",
        usuario=usuario
    )

@usuario.route("/senha", methods=["GET", "POST"])
@login_obrigatorio
def alterar_senha():

    if request.method == "POST":

        senha_atual = request.form["senha_atual"]
        nova_senha = request.form["nova_senha"]
        confirmar_senha = request.form["confirmar_senha"]

        usuario = buscar_usuario(session["usuario"])

        if not check_password_hash(usuario[4], senha_atual):
            flash("Senha atual incorreta.")
            return render_template("senha.html")

        if nova_senha != confirmar_senha:
            flash("As senhas não conferem.")
            return render_template("senha.html")

        atualizar_senha(session["usuario"], nova_senha)

        flash("Senha alterada com sucesso!")

        return redirect(url_for("usuario.alterar_senha"))

    return render_template("senha.html")

@usuario.route("/excluir", methods=["GET","POST"])
@login_obrigatorio
def excluir():
    
    if request.method == "POST":

        excluir_usuario(session["usuario"])
        session.clear()
        flash("Conta excluída.")
        return redirect(url_for("auth.login"))

    return render_template("excluir.html")

    

