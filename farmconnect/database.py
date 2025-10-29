import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

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
            telefone TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            status TEXT DEFAULT 'Pendente',
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
            codigo TEXT NOT NULL UNIQUE,
            descricao TEXT,
            imagem TEXT,
            estoque INTEGER DEFAULT 0,
            categoria_id INTEGER,
            fabricante_id INTEGER,
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
            ativo INTEGER DEFAULT 1,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id),
            FOREIGN KEY (fabricante_id) REFERENCES fabricantes(id)
        )
        """)

        # cursor.execute("ALTER TABLE medicamentos ADD COLUMN ativo INTEGER DEFAULT 1;")

        # Farmácias
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS farmacias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            bairro TEXT NOT NULL,
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
            codigo TEXT NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            status TEXT DEFAULT 'PENDENTE',
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
            total_reagendamentos INTEGER NOT NULL DEFAULT 0, 
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id),
            FOREIGN KEY(farmacia_id) REFERENCES farmacias(id)
        )
        """)

        # ReAgendamentos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reagendamentos (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            agendamento_id    INTEGER NOT NULL,
            usuario_id        INTEGER NOT NULL,
            data_antiga       TEXT NOT NULL,   -- 'YYYY-MM-DD'
            horario_antigo    TEXT NOT NULL,   -- 'HH:MM'
            data_nova         TEXT NOT NULL,
            horario_novo      TEXT NOT NULL,
            criado_em         TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),

            FOREIGN KEY (agendamento_id) REFERENCES agendamentos(id),
            FOREIGN KEY (usuario_id)     REFERENCES usuarios(id)
        )
        """)

        # Índices úteis para relatórios
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reag_agendamento ON reagendamentos(agendamento_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reag_usuario ON reagendamentos(usuario_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reag_criado_em ON reagendamentos(criado_em)")

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

        # Carrinho
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS carrinho (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                medicamento_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 1,
                data_adicao TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id)
            )
            """)

        # Cadastro de Farmácias:
        # Inserção fixa de farmácias (somente se ainda não existirem)
        cursor.execute("SELECT COUNT(*) FROM farmacias")
        if cursor.fetchone()[0] == 0:
            farmacias = [
                {
                    "nome": "Fusar",
                    "endereco": "Praça General Osório, 37 - Centro",
                    "bairro": "Centro",
                    "cnpj": "00.000.001/0001-00",
                    "cidade": "Angra dos Reis",
                    "estado": "RJ",
                    "telefone": "(24) 3368-7300"
                },
                {
                    "nome": "Farmácia Central",
                    "endereco": "Rua Moreira dos Santos, 768 - Centro",
                    "bairro": "Centro",
                    "cnpj": "00.000.002/0001-00",
                    "cidade": "Barra do Piraí",
                    "estado": "RJ",
                    "telefone": "(24) 2444-4594"
                },
                {
                    "nome": "Farmácia Municipal de Barra Mansa",
                    "endereco": "Rua Domingos Mariana, 1102 - Centro",
                    "bairro": "Centro",
                    "cnpj": "00.000.003/0001-00",
                    "cidade": "Barra Mansa",
                    "estado": "RJ",
                    "telefone": "(24) 3323-7130"
                },
                {
                    "nome": "Farmácia e Almoxarifado Central",
                    "endereco": "Rua Gonçalves da Silva, 141 - Centro (ao lado do CAPS)",
                    "bairro": "Centro",
                    "cnpj": "00.000.004/0001-00",
                    "cidade": "Bom Jesus do Itabapoana",
                    "estado": "RJ",
                    "telefone": "(22) 3831-1196"
                },
                {
                    "nome": "Farmácia de Medicamentos Excepcionais",
                    "endereco": "Av. Teixeira e Souza, 2.104 - São Cristóvão",
                    "bairro": "São Cristóvão",
                    "cnpj": "00.000.005/0001-00",
                    "cidade": "Cabo Frio",
                    "estado": "RJ",
                    "telefone": "(22) 2646-2506"
                },
                {
                    "nome": "Secretaria Municipal de Saúde",
                    "endereco": "Rua Voluntários da Pátria, 161-185 - Centro",
                    "bairro": "Centro",
                    "cnpj": "00.000.006/0001-00",
                    "cidade": "Campos dos Goytacazes",
                    "estado": "RJ",
                    "telefone": "-"
                },
                {
                    "nome": "Secretaria de Saúde de Cordeiro",
                    "endereco": "Rua Nacib Simão, 1325 - Rodolfo Gonçalves",
                    "bairro": "Rodolfo Gonçalves",
                    "cnpj": "00.000.007/0001-00",
                    "cidade": "Cordeiro",
                    "estado": "RJ",
                    "telefone": "-"
                },
                {
                    "nome": "Riofarmes Duque de Caxias",
                    "endereco": "Rua Marechal Floriano, 586 A - Bairro 25 de Agosto",
                    "bairro": "25 de Agosto",
                    "cnpj": "00.000.008/0001-00",
                    "cidade": "Duque de Caxias",
                    "estado": "RJ",
                    "telefone": "(21) 98235-0066"
                },
                {
                    "nome": "Secretaria Municipal de Saúde - Farmácia Básica",
                    "endereco": "Rua Desembargador Ferreira Pinto, 09 Fds. - Centro",
                    "bairro": "Centro",
                    "cnpj": "00.000.009/0001-00",
                    "cidade": "Itaboraí",
                    "estado": "RJ",
                    "telefone": "(21) 2645-1802"
                },
                {
                    "nome": "Famácia de Medicamentos Excepcionais",
                    "endereco": "Rua 10 de Maio nº 893 - Centro",
                    "bairro": "Centro",
                    "cnpj": "00.000.010/0001-00",
                    "cidade": "Itaperuna",
                    "estado": "RJ",
                    "telefone": "(22) 3822-6752"
                },
                {
                    "nome": "Secretaria de Saúde",
                    "endereco": "Rua Darcílio Possati 134 - Visconde de Araújo",
                    "bairro": "Visconde de Araújo",
                    "cnpj": "00.000.011/0001-00",
                    "cidade": "Macaé",
                    "estado": "RJ",
                    "telefone": "(22) 2763-6330"
                },
                {
                    "nome": "Farmácia Municipal de Volta Redonda",
                    "endereco": "Rua 545 nº 616 - Jardim Paraíba - Estádio da Cidadania, 2º andar",
                    "bairro": "Jardim Paraíba",
                    "cnpj": "00.000.012/0001-00",
                    "cidade": "Volta Redonda",
                    "estado": "RJ",
                    "telefone": "(24) 3339-9465"
                }
            ]

            for f in farmacias:
                cursor.execute("""
                    INSERT INTO farmacias (nome, endereco, bairro, cnpj, cidade, estado, telefone)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (f["nome"], f["endereco"], f["bairro"], f["cnpj"], f["cidade"], f["estado"], f["telefone"]))

        conn.commit()

def consultar_estoque_farmacia(farmacia_id, medicamento_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT quantidade FROM estoque
        WHERE farmacia_id = ? AND medicamento_id = ?
    """, (farmacia_id, medicamento_id))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else 0

def reduzir_estoque_farmacia(farmacia_id, medicamento_id, quantidade=1):
    conn = conectar()
    cursor = conn.cursor()

    # Pega quantidade anterior (para log)
    cursor.execute("""
        SELECT quantidade FROM estoque
        WHERE farmacia_id = ? AND medicamento_id = ?
    """, (farmacia_id, medicamento_id))
    atual = cursor.fetchone()
    if not atual:
        conn.close()
        return False

    anterior = atual[0]
    novo = max(anterior - quantidade, 0)

    # Atualiza estoque
    cursor.execute("""
        UPDATE estoque
        SET quantidade = ?
        WHERE farmacia_id = ? AND medicamento_id = ?
    """, (novo, farmacia_id, medicamento_id))

    # Registra log
    cursor.execute("""
        INSERT INTO estoque_logs (farmacia_id, medicamento_id, quantidade_anterior, quantidade_nova, alterado_por)
        VALUES (?, ?, ?, ?, ?)
    """, (farmacia_id, medicamento_id, anterior, novo, "Sistema"))

    conn.commit()
    conn.close()
    return True

def aprovar_usuario(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET status = 'Aprovado'
        WHERE id = ?
    """, (usuario_id,))

    conn.commit()
    cursor.close()
    conn.close()


def recusar_usuario(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET status = 'Recusado'
        WHERE id = ?
    """, (usuario_id,))

    conn.commit()
    cursor.close()
    conn.close()

def registrar_usuario(nome, email, cpf, nascimento, telefone, senha):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios (nome, email, cpf, nascimento, telefone, senha)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, email, cpf, nascimento, telefone, senha))
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
    
def buscar_dados_usuario(email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nome, cpf, nascimento, email, telefone
        FROM usuarios
        WHERE email = ?
    """, (email,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()

    if resultado:
        return {
            "nome": resultado[0],
            "cpf": resultado[1],
            "nasc": resultado[2],
            "email": resultado[3],
            "tel": resultado[4]  # opcional: você pode adicionar o campo telefone depois se estiver no banco
        }
    return None
        
def listar_medicamentos(include_inativos=True):
    conn = conectar()
    cursor = conn.cursor()

    sql = """
        SELECT 
            m.id, m.nome, m.codigo, m.descricao, m.imagem, 
            e.quantidade AS estoque,
            c.nome AS categoria, 
            f.nome AS fabricante,
            fa.nome AS farmacia,
            fa.endereco AS farmacia_endereco,
            fa.id AS farmacia_id,
            m.ativo
        FROM medicamentos m
        LEFT JOIN categorias c ON m.categoria_id = c.id
        LEFT JOIN fabricantes f ON m.fabricante_id = f.id
        LEFT JOIN estoque e ON m.id = e.medicamento_id
        LEFT JOIN farmacias fa ON e.farmacia_id = fa.id
    """

    if not include_inativos:
        sql += " WHERE m.ativo = 1"

    cursor.execute(sql)
    medicamentos = cursor.fetchall()

    cursor.close()
    conn.close()

    return medicamentos


def adicionar_estoque(farmacia_id, medicamento_id, quantidade):
    conn = conectar()
    cursor = conn.cursor()

    # Insere no estoque
    cursor.execute("""
        INSERT INTO estoque (farmacia_id, medicamento_id, quantidade)
        VALUES (?, ?, ?)
    """, (farmacia_id, medicamento_id, quantidade))

    # Registra log
    cursor.execute("""
        INSERT INTO estoque_logs (farmacia_id, medicamento_id, quantidade_anterior, quantidade_nova, alterado_por)
        VALUES (?, ?, ?, ?, ?)
    """, (farmacia_id, medicamento_id, 0, quantidade, "Cadastro inicial"))

    conn.commit()
    conn.close()

def adicionar_medicamento(codigo, nome, descricao, imagem, estoque, categoria_id=None, fabricante_id=None):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO medicamentos (codigo, nome, descricao, imagem, estoque, categoria_id, fabricante_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (codigo, nome, descricao, imagem, estoque, categoria_id, fabricante_id))

    conn.commit()
    id_medicamento = cursor.lastrowid
    cursor.close()
    conn.close()

    return id_medicamento

def desativar_medicamento(id):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE medicamentos SET ativo = 0 WHERE id = ?", (id,))

    conn.commit()
    cursor.close()
    conn.close()

def reativar_medicamento(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("UPDATE medicamentos SET ativo = 1 WHERE id = ?", (id,))

    conn.commit()
    cursor.close()
    conn.close()

def agendar_medicamento(usuario_email, medicamento_id, codigo, data, horario, status):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (usuario_email,))
    user = cursor.fetchone()

    if user:
        usuario_id = user[0]

        cursor.execute("""
            INSERT INTO agendamentos (usuario_id, medicamento_id, codigo, data, horario, status)
            VALUES (?, ?, ?, ?, ?, 'PENDENTE')
        """, (usuario_id, medicamento_id, codigo, data, horario, status))

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

def editar_medicamento(id, nome, codigo, descricao, imagem, estoque, categoria_id=None, fabricante_id=None):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE medicamentos
        SET nome = ?, codigo = ?, descricao = ?, imagem = ?, estoque = ?, categoria_id = ?, fabricante_id = ?
        WHERE id = ?
    """, (nome, codigo, descricao, imagem, estoque, categoria_id, fabricante_id, id))

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

def registrar_medicamento_reservado(usuario_id, medicamento_id, quantidade):
    from datetime import datetime, timedelta
    conn = conectar()
    cursor = conn.cursor()

    data_reserva = datetime.now().strftime("%Y-%m-%d")
    validade = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")

    for _ in range(quantidade):
        cursor.execute("""
            INSERT INTO medicamentos_reservados (usuario_id, medicamento_id, data_reserva, validade)
            VALUES (?, ?, ?, ?)
        """, (usuario_id, medicamento_id, data_reserva, validade))

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

def desativar_medicamento(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("UPDATE medicamentos SET ativo = 0 WHERE id = ?", (id,))
    
    conn.commit()
    cursor.close()
    conn.close()

def listar_farmacias():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, endereco, bairro, cnpj, cidade, estado, telefone
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

def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, email, cpf, nascimento, telefone, data_criacao, status FROM usuarios ORDER BY data_criacao DESC")

    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return usuarios

def listar_agendamentos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            a.id, 
            u.nome AS paciente, 
            m.nome AS medicamento,
            f.nome AS farmacia, 
            a.codigo,
            a.data, 
            a.horario, 
            a.quantidade,
            a.status,
            a.data_criacao
        FROM agendamentos a
        JOIN usuarios u ON a.usuario_id = u.id
        JOIN medicamentos m ON a.medicamento_id = m.id
        JOIN farmacias f ON a.farmacia_id = f.id
        ORDER BY a.data_criacao DESC
    """)

    agendamentos = cursor.fetchall()

    cursor.close()
    conn.close()

    return agendamentos

def listar_agendamentos_usuario(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            a.id, 
            m.nome AS medicamento,
            f.nome AS farmacia,
            f.endereco as endereco, 
            a.codigo,
            a.data, 
            a.horario, 
            a.status,
            a.data_criacao
        FROM agendamentos a
        JOIN medicamentos m ON a.medicamento_id = m.id
        JOIN farmacias f ON a.farmacia_id = f.id
        WHERE a.usuario_id = ?
        ORDER BY a.data_criacao DESC
    """, (usuario_id,))

    resultado = cursor.fetchall()
    conn.close()
    return resultado

def adicionar_agendamento(usuario_id, medicamento_id, farmacia_id, codigo, data, horario, status="Pendente", quantidade=1):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO agendamentos (usuario_id, medicamento_id, farmacia_id, codigo, data, horario, status, quantidade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (usuario_id, medicamento_id, farmacia_id, codigo, data, horario, status, quantidade))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print("Erro ao adicionar agendamento:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def adicionar_ao_carrinho_db(usuario_id, medicamento_id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT quantidade FROM carrinho
            WHERE usuario_id = ? AND medicamento_id = ?
        """, (usuario_id, medicamento_id))
        
        existente = cursor.fetchone()

        if existente:
            cursor.execute("""
                UPDATE carrinho
                SET quantidade = quantidade + 1
                WHERE usuario_id = ? AND medicamento_id = ?
            """, (usuario_id, medicamento_id))
        else:
            cursor.execute("""
                INSERT INTO carrinho (usuario_id, medicamento_id, quantidade)
                VALUES (?, ?, ?)
            """, (usuario_id, medicamento_id, 1))

        conn.commit()
    except Exception as e:
        print("Erro ao adicionar ao carrinho:", e)
    finally:
        cursor.close()
        conn.close()


def remover_do_carrinho_db(usuario_id, medicamento_id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM carrinho
            WHERE usuario_id = ? AND medicamento_id = ?
        """, (usuario_id, medicamento_id))
        conn.commit()
    except Exception as e:
        print("Erro ao remover do carrinho:", e)
    finally:
        cursor.close()
        conn.close()

def aumentar_quantidade_db(usuario_id, medicamento_id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE carrinho
            SET quantidade = quantidade + 1
            WHERE usuario_id = ? AND medicamento_id = ?
        """, (usuario_id, medicamento_id))
        conn.commit()
    except Exception as e:
        print("Erro ao aumentar quantidade:", e)
    finally:
        cursor.close()
        conn.close()

def diminuir_quantidade_db(usuario_id, medicamento_id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        # Verifica a quantidade atual
        cursor.execute("""
            SELECT quantidade FROM carrinho
            WHERE usuario_id = ? AND medicamento_id = ?
        """, (usuario_id, medicamento_id))
        resultado = cursor.fetchone()

        if resultado:
            quantidade = resultado[0]
            if quantidade > 1:
                cursor.execute("""
                    UPDATE carrinho
                    SET quantidade = quantidade - 1
                    WHERE usuario_id = ? AND medicamento_id = ?
                """, (usuario_id, medicamento_id))
            else:
                # Quantidade 1 → remover
                cursor.execute("""
                    DELETE FROM carrinho
                    WHERE usuario_id = ? AND medicamento_id = ?
                """, (usuario_id, medicamento_id))

        conn.commit()
    except Exception as e:
        print("Erro ao diminuir quantidade:", e)
    finally:
        cursor.close()
        conn.close()

def carregar_carrinho_usuario(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.medicamento_id, c.quantidade, m.nome, m.codigo, m.descricao, m.imagem, m.estoque
        FROM carrinho c
        JOIN medicamentos m ON c.medicamento_id = m.id
        WHERE c.usuario_id = ?
    """, (usuario_id,))
    
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()

    carrinho = []
    for linha in resultado:
        carrinho.append({
            "id": linha[0],
            "quantidade": linha[1],
            "nome": linha[2],
            "codigo": linha[3],
            "descricao": linha[4],
            "imagem": linha[5],
            "estoque": linha[6]
        })

    return carrinho

def aprovar_agendamento(agendamento_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE agendamentos
        SET status = 'Confirmado'
        WHERE id = ?
    """, (agendamento_id,))
    conn.commit()
    cursor.close()
    conn.close()

def cancelar_agendamento(agendamento_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE agendamentos
        SET status = 'Cancelado'
        WHERE id = ?
    """, (agendamento_id,))
    conn.commit()
    cursor.close()
    conn.close()

def buscar_nome_adm(email):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT nome FROM administradores WHERE email = ?", (email,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return resultado[0] if resultado else "Administrador"

def atualizar_dados_usuario(email_antigo, nome, cpf, nasc, email_novo, telefone):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE usuarios
            SET nome = ?, cpf = ?, nascimento = ?, email = ?, telefone = ?
            WHERE email = ?
        """, (nome, cpf, nasc, email_novo, telefone, email_antigo))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print("Erro ao atualizar dados do usuário:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def medicamentos_mais_solicitados(limit=5):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.nome, COUNT(*) as total
        FROM agendamentos a
        JOIN medicamentos m ON a.medicamento_id = m.id
        GROUP BY m.nome
        ORDER BY total DESC
        LIMIT ?
    """, (limit,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def confirmar_retirada_medicamento(agendamento_id):
    from datetime import datetime
    conn = conectar()
    cursor = conn.cursor()

    # Pega dados do agendamento
    cursor.execute("""
        SELECT usuario_id, medicamento_id, quantidade
        FROM agendamentos
        WHERE id = ?
    """, (agendamento_id,))
    resultado = cursor.fetchone()

    if not resultado:
        conn.close()
        return False

    usuario_id, medicamento_id, quantidade = resultado
    data_retirada = datetime.now().strftime("%Y-%m-%d")

    try:
        # Atualiza status do agendamento
        cursor.execute("""
            UPDATE agendamentos
            SET status = 'Concluído/Retirado'
            WHERE id = ?
        """, (agendamento_id,))

        # Registra na tabela de medicamentos retirados
        cursor.execute("""
            INSERT INTO medicamentos_retirados (usuario_id, medicamento_id, data_retirada)
            VALUES (?, ?, ?)
        """, (usuario_id, medicamento_id, data_retirada))

        # Remove a quantidade correspondente da tabela de reservas
        cursor.execute("""
            DELETE FROM medicamentos_reservados
            WHERE rowid IN (
                SELECT rowid FROM medicamentos_reservados
                WHERE usuario_id = ? AND medicamento_id = ?
                LIMIT ?
            )
        """, (usuario_id, medicamento_id, quantidade))

        conn.commit()
        return True
    except Exception as e:
        print("Erro ao confirmar retirada:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def listar_medicamentos_retirados(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            m.nome,
            a.data,
            a.horario,
            f.nome AS farmacia,
            f.endereco AS endereco,
            a.quantidade
        FROM agendamentos a
        JOIN medicamentos m ON a.medicamento_id = m.id
        JOIN farmacias f ON a.farmacia_id = f.id
        WHERE a.usuario_id = ? AND a.status = 'Concluído/Retirado'
        ORDER BY a.data DESC, a.horario DESC
    """, (usuario_id,))

    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado

def listar_reagendamentos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            r.id,
            u.nome AS paciente,
            m.nome AS medicamento,
            f.nome AS farmacia,
            a.codigo,
            r.data_antiga,
            r.horario_antigo,
            r.data_nova,
            r.horario_novo,
            r.criado_em
        FROM reagendamentos r
        JOIN agendamentos a ON r.agendamento_id = a.id
        JOIN usuarios u ON r.usuario_id = u.id
        JOIN medicamentos m ON a.medicamento_id = m.id
        JOIN farmacias f ON a.farmacia_id = f.id
        ORDER BY r.criado_em DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados


def verificar_status_usuario(email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM usuarios WHERE email = ?", (email,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado[0] if resultado else None


def verificar_agendamentos_vencidos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, farmacia_id, medicamento_id, quantidade
        FROM agendamentos
        WHERE status IN ('Pendente', 'Confirmado')
        AND julianday('now') - julianday(data_criacao) > 15
    """)
    vencidos = cursor.fetchall()

    for ag in vencidos:
        agendamento_id, farmacia_id, medicamento_id, quantidade = ag

        # Devolve corretamente a quantidade reservada
        cursor.execute("""
            UPDATE estoque
            SET quantidade = quantidade + ?
            WHERE farmacia_id = ? AND medicamento_id = ?
        """, (quantidade, farmacia_id, medicamento_id))

        cursor.execute("""
            UPDATE agendamentos
            SET status = 'Cancelado'
            WHERE id = ?
        """, (agendamento_id,))

    conn.commit()
    cursor.close()
    conn.close()

    # Adicionar coluna de quantidade
def add_qtd_agendamentos():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE agendamentos ADD COLUMN quantidade INTEGER DEFAULT 1")
        conn.commit()
    except sqlite3.OperationalError:
        # Já existe a coluna
        pass
    finally:
        cursor.close()
        conn.close()













