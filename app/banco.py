import sqlite3
from werkzeug.security import generate_password_hash
import os
import sqlite3

BASE_DIR = os.path.dirname(__file__)
CAMINHO_BANCO = os.path.join(BASE_DIR, "usuarios.db")

def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao
def criar_tabela(conexao):

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)

    conexao.commit()

def buscar_usuario(usuario):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM usuarios
        WHERE usuario = ?
    """, (usuario,))

    usuario_encontrado = cursor.fetchone()

    conexao.close()

    return usuario_encontrado

def cadastrar_usuario(nome, email, usuario, senha):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO usuarios
        (nome, email, usuario, senha)
        VALUES (?, ?, ?, ?)
    """, (nome, email, usuario, senha))

    conexao.commit()
    conexao.close()

def atualizar_usuario(nome, email, usuario):

    conexao = conectar()
    cursor = conexao.cursor()

    print(nome)
    print(email)
    print(usuario)

    cursor.execute("""
        UPDATE usuarios
        SET nome = ?, email = ?
        WHERE usuario = ?
    """, (nome, email, usuario))

    conexao.commit()
    conexao.close()

def atualizar_senha(usuario, senha):

    conexao = conectar()

    cursor = conexao.cursor()

    senha_hash = generate_password_hash(senha)

    cursor.execute("""
    UPDATE usuarios
    SET senha = ?
    WHERE usuario = ?
    """, (senha_hash, usuario))

    conexao.commit()

    conexao.close()

def excluir_usuario(usuario):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM usuarios
        WHERE usuario = ?
    """, (usuario,))

    conexao.commit()
    conexao.close()
