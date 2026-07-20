from functools import wraps
from flask import session, redirect, url_for


def login_obrigatorio(funcao):

    @wraps(funcao)
    def verificar_login(*args, **kwargs):

        if "usuario" not in session:
            return redirect(url_for("auth.login"))

        return funcao(*args, **kwargs)

    return verificar_login
