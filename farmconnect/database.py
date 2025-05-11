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
            senha TEXT NOT NULL,
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Admins
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS administradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
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
            estoque INTEGER DEFAULT 0,
            categoria_id INTEGER,
            fabricante_id INTEGER,
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id),
            FOREIGN KEY (fabricante_id) REFERENCES fabricantes(id)
        )
        """)


        # Farmácias
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS farmacias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            cnpj TEXT NOT NULL UNIQUE,
            cidade TEXT,
            estado TEXT,
            telefone TEXT,
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP
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

        # Logs de alteração nos estoques
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farmacia_id INTEGER NOT NULL,
        medicamento_id INTEGER NOT NULL,
        quantidade_anterior INTEGER,
        quantidade_nova INTEGER,
        alterado_por TEXT,
        data_alteracao TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (farmacia_id) REFERENCES farmacias(id),
        FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id)
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
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
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
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
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
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id)
        )
        """)

        # Notificacoes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notificacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            mensagem TEXT NOT NULL,
            lida INTEGER DEFAULT 0,
            data_envio TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
        """)

        # Categorias de medicamentos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            )
        """)

        # Fabricantes de medicamentos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fabricantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
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
        
def listar_medicamentos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT m.id, m.nome, m.descricao, m.imagem, m.estoque,
               c.nome AS categoria, f.nome AS fabricante
        FROM medicamentos m
        LEFT JOIN categorias c ON m.categoria_id = c.id
        LEFT JOIN fabricantes f ON m.fabricante_id = f.id
    """)

    medicamentos = cursor.fetchall()

    cursor.close()
    conn.close()

    return medicamentos


def adicionar_medicamento(nome, descricao, imagem, estoque, categoria_id=None, fabricante_id=None):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO medicamentos (nome, descricao, imagem, estoque, categoria_id, fabricante_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, descricao, imagem, estoque, categoria_id, fabricante_id))

    conn.commit()
    cursor.close()
    conn.close()


def agendar_medicamento(usuario_email, medicamento_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (usuario_email,))
    user = cursor.fetchone()

    if user:
        usuario_id = user[0]

        # Pegar a primeira farmacia cadastrada por enquanto
        cursor.execute("SELECT id FROM farmacias LIMIT 1")
        farmacia = cursor.fetchone()

        if farmacia:
            farmacia_id = farmacia[0]

            cursor.execute("""
                INSERT INTO agendamentos (usuario_id, medicamento_id, farmacia_id, data, horario, status)
                VALUES (?, ?, ?, DATE('now'), TIME('now'), 'PENDENTE')
            """, (usuario_id, medicamento_id, farmacia_id))

            conn.commit()

    cursor.close()
    conn.close()


def enviar_notificacao(usuario_id, mensagem):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notificacoes (usuario_id, mensagem)
        VALUES(?, ?)
    """, (usuario_id, mensagem))

    conn.commit()
    cursor.close()
    conn.close()
    
def listar_notificacoes(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, mensagem, lida, data_envio
        FROM notificacoes
        WHERE usuario_id = ?
        ORDER BY data_envio DESC
    """, (usuario_id,))

    notificacoes = cursor.fetchall()

    cursor.close()
    conn.close()

    return notificacoes

def listar_categorias():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM categorias ORDER BY nome")

    categorias = cursor.fetchall()

    cursor.close()
    conn.close()

    return categorias

def listar_fabricantes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM fabricantes ORDER BY nome")

    fabricantes = cursor.fetchall()

    cursor.close()
    conn.close()

    return fabricantes

def solicitar_notificacao(usuario_email, medicamento_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (usuario_email,))
    user = cursor.fetchone()

    if user:
        usuario_id = user[0]

        cursor.execute("""
            INSERT INTO notificacoes (usuario_id, mensagem)
            VALUES (?, ?)
        """, (usuario_id, f"O medicamento que você pediu (ID {medicamento_id}) está disponível!"))

        conn.commit()

    cursor.close()
    conn.close()

def editar_medicamento(id, nome, descricao, imagem, estoque,categoria_id=None, fabricante_id=None,):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE medicamentos
        SET nome = ?, descricao = ?, imagem = ?, estoque = ?, categoria_id = ?, fabricante_id = ? 
        WHERE id = ?
    """, (nome, descricao, imagem, estoque, categoria_id, fabricante_id, id))

    conn.commit()
    cursor.close()
    conn.close()

def reduzir_estoque_medicamento(medicamento_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE medicamentos
        SET estoque = CASE WHEN estoque > 0 THEN estoque - 1 ELSE 0 END
        WHERE id = ?
    """, (medicamento_id,))

    conn.commit()
    cursor.close()
    conn.close()

def registrar_medicamento_reservado(usuario_email, medicamento_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (usuario_email,))
    user = cursor.fetchone()

    if user:
        usuario_id = user[0]

        cursor.execute("""
            INSERT INTO medicamentos_reservados (usuario_id, medicamento_id, data_reserva)
            VALUES (?, ?, DATE('now'))
        """, (usuario_id, medicamento_id))

        conn.commit()

    cursor.close()
    conn.close()

def registrar_admin(nome, email, senha):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO administradores (nome, email, senha)
            VALUES (?, ?, ?)
        """, (nome, email, senha))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print("Erro ao cadastrar administrador:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def verificar_login_admin(email, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM administradores
        WHERE email = ? AND senha = ?
    """, (email, senha))

    admin = cursor.fetchone()

    cursor.close()
    conn.close()

    return admin is not None

def adicionar_fabricante(nome):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO fabricantes (nome) VALUES (?)
        """, (nome,))
        conn.commit()

    except sqlite3.IntegrityError:
        print(f"Fabricante '{nome}' já existe.")
    finally:
        cursor.close()
        conn.close()

def adicionar_categoria(nome):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO categorias (nome) VALUES (?)
        """, (nome,))
        conn.commit()

    except sqlite3.IntegrityError:
        print(f"Categoria '{nome}' já existe.")
    finally:
        cursor.close()
        conn.close()

def deletar_medicamento(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM medicamentos WHERE id = ?", (id,))
    
    conn.commit()
    cursor.close()
    conn.close()

def listar_farmacias():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, endereco, cnpj, cidade, estado, telefone
        FROM farmacias
        ORDER BY nome
    """)
    farmacias = cursor.fetchall()

    cursor.close()
    conn.close()

    return farmacias


def adicionar_farmacia(nome, endereco, cnpj, cidade, estado, telefone):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO farmacias (nome, endereco, cnpj, cidade, estado, telefone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, endereco, cnpj, cidade, estado, telefone))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("Erro ao adicionar farmácia:", e)
    finally:
        cursor.close()
        conn.close()


def editar_farmacia(id, nome, endereco, cnpj, cidade, estado, telefone):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE farmacias
        SET nome = ?, endereco = ?, cnpj = ?, cidade = ?, estado = ?, telefone = ?
        WHERE id = ?
    """, (nome, endereco, cnpj, cidade, estado, telefone, id))

    conn.commit()
    cursor.close()
    conn.close()


def deletar_farmacia(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM farmacias WHERE id = ?", (id,))
    
    conn.commit()
    cursor.close()
    conn.close()












