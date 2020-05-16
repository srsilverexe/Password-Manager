import sqlite3
import os

CLEAR = 'cls' if os.name == 'nt' else 'clear' 
limpa_tela = lambda : os.system(CLEAR)

master_password = ("")

senha = input("Insira sua senha master: ")
if senha != master_password:
    print("Senha invalida! Encerando...")
    exit()

conn = sqlite3.connect('password.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    master TEXT NOT NULL,
    service TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
''')

def Menu():
    print("********************************")
    print("* i : inserir nova senha       *")
    print("* l : listar servicos salvos   *")
    print("* r : recuperar uma senha      *")
    print("* s : sair                     *")
    print("********************************")


def get_password(service):
    cursor.execute(f'''
        SELECT username, password FROM users
        WHERE service = '{service}'
    ''')

    if cursor.rowcount == 0:
        print("Serviço não cadastrado (use 'l' para ver os serviços disponiveis)")
    else:
        for user in cursor.fetchall():
            print(user)

def insert_password(service, username, password):
    cursor.execute(f'''
        INSERT INTO users (service, username, password)
        VALUES ('{service}', '{username}', '{password}')
    ''')
    conn.commit()

def show_services():
    cursor.execute('''
        SELECT service FROM users;
    ''')
    for service in cursor.fetchall():
        print(service)

while True:
    limpa_tela()
    Menu()
    op = input("oque deseja fazer?  ")
    if op not in ['i', 'l', 'r', 's']:
        limpa_tela()
        print("açao invalida!")
        continue

    if op == 's':
        break

    if op == 'i':
        limpa_tela()
        service = input('Qual e o nome do serviço? ')
        username = input('Qual e o nome de usuario/email? ')
        password = input('Qual e a senha? ')
        insert_password(service, username, password)

    if op == 'l':
        limpa_tela()
        show_services()
    
    if op == 'r':
        limpa_tela()
        service = input("Quar serviço deseja a senha?")
        get_password(service)


    input('precione qualquer tecla')

if __name__ == '__main__':
    Menu()
conn.close()