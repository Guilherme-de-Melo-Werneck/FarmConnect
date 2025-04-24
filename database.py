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
        )
        """)

        # Medicamentos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            imagem TEXT,
            estoque INTEGER DEFAULT 0
        )
        """)

        # Farmácias
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS farmacias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            cidade TEXT,
            estado TEXT,
            telefone TEXT
        )
        """)

        # Estoque por farmácia
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicamento_id INTEGER NOT NULL,
            farmacia_id INTEGER NOT NULL,
            quantidade INTEGER DEFAULT 0,
            FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id),
            FOREIGN KEY(farmacia_id) REFERENCES farmacias(id)
        )
        """)

        # Agendamentos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            medicamento_id INTEGER NOT NULL,
            farmacia_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            status TEXT DEFAULT 'PENDENTE',
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id),
            FOREIGN KEY(farmacia_id) REFERENCES farmacias(id)
        )
        """)

        # Medicamentos Reservados
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos_reservados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            medicamento_id INTEGER NOT NULL,
            data_reserva TEXT NOT NULL,
            validade TEXT,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id)
        )
        """)

        # Medicamentos Retirados
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos_retirados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            medicamento_id INTEGER NOT NULL,
            data_retirada TEXT NOT NULL,
            observacoes TEXT,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id)
        )
        """)

        conn.commit()

def registrar_usuario(nome, email, cpf, nascimento, senha):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios (nome, email, cpf, nascimento, senha)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, email, cpf, nascimento, senha))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print("Erro ao cadastrar usuário:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def verificar_login(email, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM usuarios
        WHERE email = ? AND senha = ?
    """, (email, senha))

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return usuario is not None #  retorna True se o login for válido e False se estiver errado.

def buscar_nome_usuario(email):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT nome FROM usuarios WHERE email = ?", (email,))

    nome = cursor.fetchone()

    cursor.close()
    conn.close()

    if nome:
        return nome[0]
    else:
        return None
        