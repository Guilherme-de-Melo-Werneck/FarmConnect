import mysql.connector

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '29112001',
    'database': 'farmconnect'
}

def conectar():
    return mysql.connector.connect(**config)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        cpf VARCHAR(14) NOT NULL UNIQUE,
        nascimento VARCHAR(10) NOT NULL,
        senha VARCHAR(100) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicamentos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        descricao TEXT,
        imagem TEXT,
        estoque INT DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farmacias (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100),
        endereco TEXT,
        cidade VARCHAR(50),
        estado VARCHAR(2),
        telefone VARCHAR(20)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estoque (
        id INT AUTO_INCREMENT PRIMARY KEY,
        medicamento_id INT NOT NULL,
        farmacia_id INT NOT NULL,
        quantidade INT DEFAULT 0,
        FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id),
        FOREIGN KEY(farmacia_id) REFERENCES farmacias(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT NOT NULL,
        medicamento_id INT NOT NULL,
        farmacia_id INT NOT NULL,
        data DATE NOT NULL,
        horario TIME NOT NULL,
        status VARCHAR(20) DEFAULT 'PENDENTE',
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id),
        FOREIGN KEY(farmacia_id) REFERENCES farmacias(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicamentos_reservados (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT NOT NULL,
        medicamento_id INT NOT NULL,
        data_reserva DATE NOT NULL,
        validade DATE,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicamentos_retirados (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT NOT NULL,
        medicamento_id INT NOT NULL,
        data_retirada DATE NOT NULL,
        observacoes TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()


