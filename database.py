import sqlite3
from pathlib import Path

DB_FILE = Path("farmconnect.db")

def conectar():
    return sqlite3.connect(DB_FILE)

def criar_tabelas():
    with conectar() as conn:
        cursor = conn.cursor()

        # Usuários
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            cpf TEXT NOT NULL UNIQUE,
            nascimento TEXT NOT NULL,
            senha TEXT NOT NULL
        )""")

        # Medicamentos disponíveis
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            imagem TEXT,
            estoque INTEGER DEFAULT 0
        )""")

        # Agendamentos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            medicamento_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            status TEXT DEFAULT 'PENDENTE',  -- PENDENTE | CONCLUÍDO | CANCELADO
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id)
        )""")

        # Medicamentos reservados
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos_reservados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            medicamento_id INTEGER NOT NULL,
            data_reserva TEXT NOT NULL,
            validade TEXT, -- por quanto tempo a reserva é válida
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id)
        )""")

        # Medicamentos retirados
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos_retirados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            medicamento_id INTEGER NOT NULL,
            data_retirada TEXT NOT NULL,
            observacoes TEXT,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id)
        )""")

        conn.commit()
