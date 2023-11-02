import psycopg2
from prettytable import PrettyTable

class Connection:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="projetoBD",
            user="postgres",
            password="2110",
            host="localhost"
        )
        self.cur = self.conn.cursor()

    def execute(self, sql, args):
        self.cur.execute(sql, args)

    def commit(self):
        self.conn.commit()

    def query(self, sql, args):
        self.cur.execute(sql, args)
        return self.cur.fetchone()

    def close(self):
        self.cur.close()
        self.conn.close()
    
    def customer_exists(self, cpf):
        self.cur.execute("SELECT cpf FROM cliente WHERE cpf = %s", (cpf,))
        return self.cur.fetchone() is not None    
        
class ProdutoApp:
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        try:
            conn = Connection()
            conn.execute("SELECT * FROM produto", ())
            rows = conn.cur.fetchall()
            
            # Create a PrettyTable instance
            table = PrettyTable()
            
            # Add column names (these should match your database)
            table.field_names = ["cod_produto", "quantidade", "validade","fabricante", "valor", "marca","fabricado em mari"]
            
            # Add rows to the table
            for row in rows:
                table.add_row(row)
            
            # Print the table
            print(table)
            
            conn.close()
        except Exception as e:
            print("Erro ao buscar dados:", str(e))
            
def fazer_compra():
    conn = Connection()

    try:
        while True:
            # Carregar dados da tabela de produtos
            conn.execute("SELECT * FROM produto", ())
            rows = conn.cur.fetchall()

            # Criar uma tabela PrettyTable para exibir os produtos disponíveis
            table = PrettyTable()
            table.field_names = ["cod_produto", "quantidade", "validade", "fabricante", "valor", "marca", "fabricado em mari"]

            for row in rows:
                table.add_row(row)

            # Exibir a tabela de produtos
            print("Produtos disponíveis:")
            print(table)

            # Solicitar ao usuário o código do produto e a quantidade desejada
            cod_produto = int(input("Digite o código do produto que deseja comprar: "))
            quantidade = int(input("Digite a quantidade desejada: "))

            # Verificar se o produto e a quantidade escolhidos estão disponíveis
            for row in rows:
                if row[0] == cod_produto:
                    if quantidade <= row[1]:
                        print(f"Produto '{row[5]}' adicionado ao carrinho.")
                        
                        # Atualizar o estoque do produto
                        sql = "UPDATE produto SET quant_estoque = quant_estoque - %s WHERE cod_produto = %s;"
                        conn.execute(sql, (quantidade, cod_produto))
                        conn.commit()
                        
                        break
                    else:
                        print("Quantidade insuficiente em estoque.")
                        return
            else:
                print("Produto não encontrado.")
                return

            # Perguntar ao usuário se ele quer continuar comprando
            continuar = input("Deseja continuar comprando? (s/n): ")
            if continuar.lower() != 's':
                break

        # Perguntar ao usuário se ele é um cliente antigo ou novo
        cliente_novo = input("Você é um cliente novo ou antigo? (n/a): ")
        
        if cliente_novo.lower() == 'n':
            # Se for um novo cliente, chamar a função para cadastrar um novo cliente
            ClienteForm().submit()
        
        
        elif cliente_novo.lower() == 'a':
            # Se for um cliente antigo, solicitar o CPF e registrar a compra para esse CPF
            cpf_cliente = input("Por favor, digite seu CPF: ")
            
        if conn.customer_exists(cpf_cliente):
            print("Bem-vindo de volta!")
            # Aqui você pode adicionar a lógica para registrar a compra para o CPF fornecido
        else:
            print("Parece que você é um novo cliente. Vamos fazer seu cadastro.")
            ClienteForm().submit()
            # Aqui você pode adicionar a lógica para registrar a compra para o novo CPF

    except Exception as e:
        print("Erro ao fazer a compra:", str(e))
    finally:
        conn.close()  

class Compra:
    def __init__(self, cpf_cliente, cpf_vendedor):
        self.cpf_cliente = cpf_cliente
        self.cpf_vendedor = cpf_vendedor
        self.itens = []
        self.forma_pagamento = None
        self.conn = Connection()

    def adicionar_item(self, id_produto, quantidade):
        sql = "SELECT estoque FROM produto WHERE id = %s;"
        estoque = self.conn.query(sql, (id_produto,))
        if estoque < quantidade:
            print("Produto fora de estoque!")
            return
        self.itens.append((id_produto, quantidade))

    def definir_forma_pagamento(self, tipo, status):
        self.forma_pagamento = (tipo, status)

    def efetivar_compra(self):
        if not self.itens:
            print("Nenhum item na compra!")
            return
        if not self.forma_pagamento:
            print("Forma de pagamento não definida!")
            return
        for id_produto, quantidade in self.itens:
            sql = "UPDATE produto SET estoque = estoque - %s WHERE id = %s;"
            self.conn.execute(sql, (quantidade, id_produto))
        
        sql = "INSERT INTO compra (cpf_cliente, cpf_vendedor) VALUES (%s, %s) RETURNING id;"
        id_compra = self.conn.query(sql, (self.cpf_cliente, self.cpf_vendedor))
        
        for id_produto, quantidade in self.itens:
            sql = "INSERT INTO item_compra (id_compra, id_produto, quantidade) VALUES (%s, %s, %s);"
            self.conn.execute(sql, (id_compra[0], id_produto, quantidade))
        
        sql = "INSERT INTO forma_pagamento (id_compra, tipo, status) VALUES (%s, %s, %s);"
        self.conn.execute(sql, (id_compra[0],) + self.forma_pagamento)
        
    def get_desconto(self):
        sql = "SELECT timefutebol, animefavorito, cidade FROM cliente WHERE cpf = %s;"
        timefutebol, animefavorito, cidade = self.conn.query(sql, (self.cpf,))
        desconto = 0
        if timefutebol == 'Flamengo':
            desconto += 0.05  # 5% de desconto
        if animefavorito == 'One Piece':
            desconto += 0.05  # 5% de desconto
        if cidade == 'Sousa':
            desconto += 0.05  # 5% de desconto
        return desconto

    def close(self):
        self.conn.close()

class ClienteForm:
    def submit(self):
        nome = input("Nome: ")
        cpf = input("CPF: ")
        sexo = input("Sexo: ")
        email = input("Email: ")
        cidade = input("Cidade: ")
        timefutebol = input("Time de Futebol: ")
        animefavorito = input("Anime Favorito: ")

        insert_cliente(nome, cpf, sexo, email, cidade, timefutebol, animefavorito)

def insert_cliente(nome, cpf, sexo, email, cidade, timefutebol, animefavorito):
    try:
        conn = Connection()
        
        sql = "INSERT INTO cliente (nome, cpf, sexo, email, cidade, timefutebol, animefavorito) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        conn.execute(sql, (nome, cpf, sexo, email, cidade, timefutebol, animefavorito))

        conn.commit()
        conn.close()
        print("Cliente inserido com sucesso!")

    except Exception as e:
        print("Erro ao inserir cliente:", str(e))   

class Cliente:
    def __init__(self, cpf):
        self.cpf = cpf
        self.conn = Connection()

    def get_dados_cadastrais(self):
        sql = "SELECT * FROM cliente WHERE cpf = %s;"
        return self.conn.query(sql, (self.cpf,))
        
    def get_pedidos(self):
        sql = "SELECT * FROM pedido WHERE cpf_cliente = %s;"
        return self.conn.query(sql, (self.cpf,))
        
    def get_desconto(self):
        sql = "SELECT timefutebol, animefavorito, cidade FROM cliente WHERE cpf = %s;"
        timefutebol, animefavorito, cidade = self.conn.query(sql, (self.cpf,))
        desconto = 0
        if timefutebol == 'Flamengo':
            desconto += 0.05  # 5% de desconto
        if animefavorito == 'One Piece':
            desconto += 0.05  # 5% de desconto
        if cidade == 'Sousa':
            desconto += 0.05  # 5% de desconto
        return desconto

    def close(self):
        self.conn.close()
        
class FormaPagamentoForm:
    def submit(self):
        tipo = input("Tipo de pagamento (Cartão, Boleto, Pix, Berries): ")
        status = input("Status: ")

        # Verifique se a forma de pagamento é válida
        if tipo not in ["Cartão", "Boleto", "Pix", "Berries"]:
            print("Forma de pagamento inválida. Por favor, escolha entre Cartão, Boleto, Pix e Berries.")
            return

        insert_forma_pagamento(tipo, status)

def insert_forma_pagamento(tipo, status):
    try:
        conn = Connection()
        
        sql = "INSERT INTO FormaPagamento (tipo, status) VALUES (%s, %s);"
        conn.execute(sql, (tipo, status))
        
        conn.commit()
        conn.close()
        print("Forma de pagamento inserida com sucesso!")

    except Exception as e:
        print("Erro ao inserir forma de pagamento:", str(e))

class ProdutoForm:
    def submit(self):
        nome = input("Nome do Produto: ")
        preco = float(input("Preço do Produto: "))
        quantidade = int(input("Quantidade em Estoque: "))

        insert_produto(nome, preco, quantidade)

def insert_produto(nome, preco, quantidade):
    try:
        conn = Connection()
        
        sql = "INSERT INTO Produto (nome, preco, estoque) VALUES (%s, %s, %s);"
        conn.execute(sql, (nome, preco, quantidade))
        
        conn.commit()
        conn.close()
        print("Produto inserido com sucesso!")

    except Exception as e:
        print("Erro ao inserir produto:", str(e))

class Vendedor:
    def __init__(self, cpf):
        self.cpf = cpf
        self.conn = Connection()

    def get_vendas(self):
        sql = "SELECT * FROM venda WHERE cpf_vendedor = %s;"
        return self.conn.query(sql, (self.cpf,))
        
    def close(self):
        self.conn.close()

def gerar_relatorio_vendas():
    conn = Connection()
    sql = "SELECT cpf_vendedor, COUNT(*), SUM(valor) FROM venda GROUP BY cpf_vendedor;"
    relatorio = conn.query(sql)
    conn.close()
    return relatorio    

class Cliente:
    def __init__(self, cpf):
        self.cpf = cpf
        self.conn = Connection()

    def get_dados_cadastrais(self):
        sql = "SELECT * FROM cliente WHERE cpf = %s;"
        return self.conn.query(sql, (self.cpf,))
        
    def get_pedidos(self):
        sql = "SELECT * FROM pedido WHERE cpf_cliente = %s;"
        return self.conn.query(sql, (self.cpf,))
        
    def get_desconto(self):
        sql = "SELECT timefutebol, animefavorito, cidade FROM cliente WHERE cpf = %s;"
        timefutebol, animefavorito, cidade = self.conn.query(sql, (self.cpf,))
        desconto = 0
        if timefutebol == 'Flamengo':
            desconto += 0.05  # 5% de desconto
        if animefavorito == 'One Piece':
            desconto += 0.05  # 5% de desconto
        if cidade == 'Sousa':
            desconto += 0.05  # 5% de desconto
        return desconto

    def close(self):
        self.conn.close()

class Menu:
    def __init__(self):
        self.app = ProdutoApp()
        self.cliente_form = ClienteForm()
        self.forma_pagamento_form = FormaPagamentoForm()
        self.produto_form = ProdutoForm()

    def run(self):
        while True:
            print("Digite 1 para realizar uma compra")
            print("Digite 2 para ver se um produto esta no estoque")
            print("Digite 3 para fazer um relatorio do funcionario")
            print("Digite 0 para sair")
            
            opcao = int(input("Escolha uma opção: "))
            
            if opcao == 1:
                fazer_compra()  # Primeiro, selecione os itens para comprar
                self.cliente_form.submit()  # Em seguida, faça o cadastro do cliente
                self.forma_pagamento_form.submit()
                self.produto_form.submit()
                continue  # This will skip the rest of the loop and start from the beginning
            elif opcao == 2:
                cod_produto = int(input("Digite o código do produto que deseja verificar: "))
                conn = Connection()
                sql = "SELECT estoque FROM produto WHERE id = %s;"
                estoque = conn.query(sql, (cod_produto,))
                if estoque is not None:
                    print(f"O produto com código {cod_produto} tem {estoque} unidades em estoque.")
                else:
                    print("Produto não encontrado.")
                conn.close()
            elif opcao == 3:
                relatorio = gerar_relatorio_vendas()
                print("Relatório de vendas:")
                for linha in relatorio:
                    print(linha)
            elif opcao == 0:
                break
            else:
                print("Opção inválida. Tente novamente.")



if __name__ == "__main__":
    menu = Menu()
    menu.run()


