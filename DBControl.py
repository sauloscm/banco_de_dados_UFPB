import psycopg2 as db
import csv

class Config:
    def __init__(self):
        self.config = {
            "DBProject": {
                "user": "postgres",
                "password": "1234",
                "host": "localhost",
                "port": "5432",
                "database": "DBProject"
            }
        }

class Connection(Config):
    def __init__(self):
        Config.__init__(self)
        self.conn = db.connect(**self.config["DBProject"])
        self.cur = self.conn.cursor()


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self.conn

    @property
    def cursor(self):
        return self.cur

    def commit(self):
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

class Cliente(Connection):
    def __init__(self):
        Connection.__init__(self)

    def insert(self, *args):
        sql = "INSERT INTO cliente (nome, cpf, sexo, email) VALUES (%s, %s, %s, %s);"
        self.execute(sql, args)
        self.commit()

    def delete(self, id):
        try:
            sql_s = f"SELECT * FROM cliente WHERE cod_cliente = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para deletar."
            sql_d = f"DELETE FROM cliente WHERE cod_cliente = {id}"
            self.execute(sql_d)
            self.commit()
            return "Registro deletado"
        except Exception as e:
            print("Erro ao deletar", e)

    def update(self, id, *args):
        try:
            sql = f"UPDATE cliente SET nome = %s, cpf = %s, sexo = %s, email = %s WHERE cod_cliente = {id}"
            self.execute(sql, args)
            self.commit()
            print("Registro atualizado")
        except Exception as e:
            print("Erro ao atualizar", e)

    def search(self, *args, column="cod_cliente"):
        sql =  "SELECT * FROM cliente WHERE cod_cliente = %s"
        if column == "nome":
            sql = "SELECT * FROM cliente WHERE nome LIKE %s"
        if column == "cpf":
            sql = "SELECT * FROM cliente WHERE cpf LIKE %s"
        if column == "sexo":
            sql = "SELECT * FROM cliente WHERE sexo = %s"
        if column == "email":
            sql = "SELECT * FROM cliente WHERE email LIKE %s"
        if column == "todos":
            sql = "SELECT * FROM cliente"
        data = self.query(sql, args)

        if data:
            return data
        return "Registro não encontrado"

    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding="utf-8"))
            for row in data:
                self.insert(row["nome, cpf, sexo, email"])
            print("Registro inserido")
        except Exception as e:
            print("Erro ao inserir")

class Funcionario(Connection):
    def __init__(self):
        Connection.__init__(self)

    def insert(self, *args):
        sql = "INSERT INTO funcionario (nome, cpf, sexo, email, salario, funcao, comissoes) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        self.execute(sql, args)
        self.commit()

    def delete(self, id):
        try:
            sql_s = f"SELECT * FROM funcionario WHERE cod_funcionario = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para deletar."
            sql_d = f"DELETE FROM funcionario WHERE cod_funcionario = {id}"
            self.execute(sql_d)
            self.commit()
            return "Registro deletado"
        except Exception as e:
            print("Erro ao deletar", e)

    def update(self, id, *args):
        try:
            sql = f"UPDATE funcionario SET nome = %s, cpf = %s, sexo = %s, email = %s, salario = %s, funcao = %s, comissoes = %s WHERE cod_funcionario = {id}"
            self.execute(sql, args)
            self.commit()
            print("Registro atualizado")
        except Exception as e:
            print("Erro ao atualizar", e)

    def search(self, *args, column="cod_funcionario"):
        sql =  "SELECT * FROM funcionario WHERE cod_funcionario = %s"
        if column == "nome":
            sql = "SELECT * FROM funcionario WHERE nome LIKE %s"
        if column == "cpf":
            sql = "SELECT * FROM funcionario WHERE cpf LIKE %s"
        if column == "sexo":
            sql = "SELECT * FROM funcionario WHERE sexo = %s"
        if column == "email":
            sql = "SELECT * FROM funcionario WHERE email LIKE %s"
        if column == "salario":
            sql = "SELECT * FROM funcionario WHERE salario LIKE %s"
        if column == "funcao":
            sql = "SELECT * FROM funcionario WHERE funcao LIKE %s"
        if column == "comissoes":
            sql = "SELECT * FROM funcionario WHERE comissoes LIKE %s"
        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"


    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding="utf-8"))
            for row in data:
                self.insert(row["nome, cpf, sexo, email, salario, funcao, comissoes"])
            print("Registro inserido")
        except Exception as e:
            print("Erro ao inserir")

class Produto(Connection):
    def __init__(self):
        Connection.__init__(self)

    def insert(self, *args):
        sql = "INSERT INTO produto (quant_estoque, validade, fabricante, valor, marca) VALUES (%s, %s, %s, %s, %s);"
        self.execute(sql, args)
        self.commit()

    def delete(self, id):
        try:
            sql_s = f"SELECT * FROM produto WHERE cod_produto = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para deletar."
            sql_d = f"DELETE FROM produto WHERE cod_produto = {id}"
            self.execute(sql_d)
            self.commit()
            return "Registro deletado"
        except Exception as e:
            print("Erro ao deletar", e)

    def update(self, id, *args):
        try:
            sql = f"UPDATE produto SET quant_estoque = %s, validade = %s, fabricante = %s, valor = %s, marca = %s WHERE cod_produto = {id}"
            self.execute(sql, args)
            self.commit()
            print("Registro atualizado")
        except Exception as e:
            print("Erro ao atualizar", e)

    def search(self, *args, column="cod_produto"):
        sql =  "SELECT * FROM produto WHERE cod_produto = %s"
        if column == "quant_estoque":
            sql = "SELECT * FROM produto WHERE quant_estoque = %s"
        if column == "validade":
            sql = "SELECT * FROM produto WHERE validade LIKE %s"
        if column == "fabricante":
            sql = "SELECT * FROM produto WHERE fabricante LIKE %s"
        if column == "valor":
            sql = "SELECT * FROM produto WHERE valor LIKE %s"
        if column == "marca":
            sql = "SELECT * FROM produto WHERE marca LIKE %s"
        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"


    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding="utf-8"))
            for row in data:
                self.insert(row["quant_estoque, validade, fabricante, valor, marca"])
            print("Registro inserido")
        except Exception as e:
            print("Erro ao inserir")

class ItensVendas(Connection):
    def __init__(self):
        Connection.__init__(self)

    def insert(self, *args):
        sql = "INSERT INTO itens_vendas (cod_produto, tipo, quant_comp) VALUES (%s, %s, %s);"
        self.execute(sql, args)
        self.commit()

    def delete(self, id):
        try:
            sql_s = f"SELECT * FROM itens_vendas WHERE cod_itens = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para deletar."
            sql_d = f"DELETE FROM itens_vendas WHERE cod_itens = {id}"
            self.execute(sql_d)
            self.commit()
            return "Registro deletado"
        except Exception as e:
            print("Erro ao deletar", e)

    def update(self, id, *args):
        try:
            sql = f"UPDATE itens_vendas SET cod_produto = %s, tipo = %s, quant_comp = %s WHERE cod_itens = {id}"
            self.execute(sql, args)
            self.commit()
            print("Registro atualizado")
        except Exception as e:
            print("Erro ao atualizar", e)

    def search(self, *args, column="cod_itens"):
        sql =  "SELECT * FROM itens_vendas WHERE cod_itens = %s"
        if column == "cod_produto":
            sql = "SELECT * FROM itens_vendas WHERE cod_produto = %s"
        if column == "tipo":
            sql = "SELECT * FROM itens_vendas WHERE tipo LIKE %s"
        if column == "quant_comp":
            sql = "SELECT * FROM itens_vendas WHERE quant_comp LIKE %s"

        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"

    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding="utf-8"))
            for row in data:
                self.insert(row["cod_produto, tipo, quant_comp"])
            print("Registro inserido")
        except Exception as e:
            print("Erro ao inserir")

class Vendas(Connection):
    def __init__(self):
        Connection.__init__(self)

    def insert(self, *args):
        sql = "INSERT INTO vendas (cod_itens, cod_funcionario, cod_cliente, cod_produto, num_mesa, valor_comissão, quant_produto, valor_compra, data_) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        self.execute(sql, args)
        self.commit()

    def delete(self, id):
        try:
            sql_s = f"SELECT * FROM vendas WHERE cod_vendas = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para deletar."
            sql_d = f"DELETE FROM vendas WHERE cod_vendas = {id}"
            self.execute(sql_d)
            self.commit()
            return "Registro deletado"
        except Exception as e:
            print("Erro ao deletar", e)

    def update(self, id, *args):
        try:
            sql = f"UPDATE vendas SET cod_itens = %s, cod_funcionario = %s, cod_cliente = %s, cod_produto = %s, num_mesa = %s, valor_comissão = %s, quant_produto =%s, valor_compra = %s, data_ =%s WHERE cod_vendas = {id}"
            self.execute(sql, args)
            self.commit()
            print("Registro atualizado")
        except Exception as e:
            print("Erro ao atualizar", e)

    def search(self, *args, column="cod_vendas"):
        sql =  "SELECT * FROM vendas WHERE cod_vendas = %s"
        if column == "cod_itens":
            sql = "SELECT * FROM vendas WHERE cod_itens = %s"
        if column == "cod_funcionario":
            sql = "SELECT * FROM vendas WHERE cod_funcionario = %s"
        if column == "cod_cliente":
            sql = "SELECT * FROM vendas WHERE cod_cliente = %s"
        if column == "cod_produto":
            sql = "SELECT * FROM vendas WHERE cod_produto = %s"
        if column == "num_mesa":
            sql = "SELECT * FROM vendas WHERE num_mesa = %s"
        if column == "valor_comissão":
            sql = "SELECT * FROM vendas WHERE valor_comissão LIKE %s"
        if column == "quant_produto":
            sql = "SELECT * FROM vendas WHERE quant_produto = %s"
        if column == "valor_compra":
            sql = "SELECT * FROM vendas WHERE valor_compra LIKE %s"
        if column == "data_":
            sql = "SELECT * FROM vendas WHERE data_ LIKE %s"
        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"

    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding="utf-8"))
            for row in data:
                self.insert(row["cod_itens, cod_funcionario, cod_cliente, cod_produto, num_mesa, valor_comissão, quant_produto, valor_compra, data_"])
            print("Registro inserido")
        except Exception as e:
            print("Erro ao inserir")







def exibir_menu():
    print("Selecione uma opção:")
    print("1. Inserir")
    print("2. Atualizar")
    print("3. Excluir")
    print("4. Pesquisar por")
    print("5. Listar todos")
    print("6. Exibir um")
    print("7. Gerar relatório")
    print("0. Sair")

def menu_inserir():
    nome = input("Digite o nome do cliente: ")
    cpf = input("Digite o cpf do cliente: ")
    sexo = input("Digite o sexo do cliente: ")
    email = input("Digite o email do cliente: ")
    client.insert(nome, cpf, sexo, email)

def menu_atualizar():
    id_update = input("Digite o id do cliente que quer atualizar: ")
    nome = input("Digite o novo nome do cliente: ")
    cpf = input("Digite o novo cpf do cliente: ")
    sexo = input("Digite o novo sexo do cliente: ")
    email = input("Digite o novo email do cliente: ")
    client.update(id_update, nome, cpf, sexo, email)

def menu_excluir():
    id_delete = input("Digite o id do cliente que quer deletar: ")
    client.delete(id_delete)

def menu_pesquisar_por():
    print("1. Nome")
    print("2. CPF")
    print("3. Sexo")
    print("4. Email")
    valor_de_pesquisa = input("Selecione uma opção de pesquisa: ")
    if valor_de_pesquisa == "1":
        aux_pesquisa = input("Digite o Nome que deseja pesquisar: ")
        client.search("nome", aux_pesquisa)
    elif valor_de_pesquisa == "2":
        aux_pesquisa = input("Digite o CPF que deseja pesquisar: ")
        client.search("cpf", aux_pesquisa)
    elif valor_de_pesquisa == "3":
        aux_pesquisa = input("Digite o Sexo que deseja pesquisar: ")
        client.search("sexo", aux_pesquisa)
    elif valor_de_pesquisa == "4":
        aux_pesquisa = input("Digite o Email que deseja pesquisar: ")
        client.search("email", aux_pesquisa)

def menu_listar_todos():
    client.search(0, "todos")

def menu_exibir_um():
    valor_de_pesquisa = input("Digite o id que deseja pesquisar: ")
    client.search(valor_de_pesquisa)

#def menu_gerar_relatorio():

if __name__ == "__main__":
    client = Cliente()
    while True:
        exibir_menu()
        opcao = input("Opção: ")

        if opcao == "1":
            menu_inserir()

        elif opcao == "2":
            menu_atualizar()

        elif opcao == "3":
            menu_excluir()

        elif opcao == "4":
            menu_pesquisar_por()

        elif opcao == "5":
            menu_listar_todos()

        elif opcao == "6":
            menu_exibir_um()

        #elif opcao == "7":
            #menu_gerar_relatorio()

        elif opcao == "0":
            break

        else:
            print("Opção inválida. Tente novamente.")



# if __name__ == "__main__":
#     #client = Cliente()
#     #client.insert("Carlaum", "123.234.345-90", "F", "test@gmail.com")
#     #client.delete(4)
#     #client.update(7, "edu", "123455636", "M", "t@uolpocutom")
#     client = Cliente()
#     menu_inserir()
