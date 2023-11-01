import tkinter as tk
import psycopg2

class Connection:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="dbproject",
            user="postgres",
            password="12345678",
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

class Compra(Connection):
    def insert(self, *args):
        sql = "INSERT INTO Compra (cliente_id, vendedor_id, forma_pagamento_id) VALUES (%s, %s, %s);"
        self.execute(sql, args)
        self.commit()

    # Adicione aqui os métodos delete(), update(), search(), etc.

def verificar_estoque(self, produto_id, quantidade):
    sql = "SELECT estoque FROM Produto WHERE id = %s;"
    estoque_atual = self.query(sql, (produto_id,))

    if estoque_atual >= quantidade:
        return True
    else:
        return False

def insert(self, cliente_id, vendedor_id, forma_pagamento_id, produto_id, quantidade):
    if self.verificar_estoque(produto_id, quantidade):
        sql = "INSERT INTO Compra (cliente_id, vendedor_id, forma_pagamento_id) VALUES (%s, %s, %s);"
        self.execute(sql, (cliente_id, vendedor_id, forma_pagamento_id))
        self.commit()

        # Atualize o estoque do produto
        sql = "UPDATE Produto SET estoque = estoque - %s WHERE id = %s;"
        self.execute(sql, (quantidade, produto_id))
        self.commit()

        return True
    else:
        return False  # Não foi possível efetivar a compra devido à falta de estoque

def calcular_desconto(self, cliente_id):
    sql = "SELECT torce_flamengo, assiste_one_piece, e_de_sousa FROM Cliente WHERE id = %s;"
    cliente = self.query(sql, (cliente_id,))
    
    desconto = 0
    if cliente.torce_flamengo:
        desconto += 0.1  # Desconto de 10% para quem torce pelo Flamengo
    if cliente.assiste_one_piece:
        desconto += 0.1  # Desconto de 10% para quem assiste One Piece
    if cliente.e_de_sousa:
        desconto += 0.1  # Desconto de 10% para quem é de Sousa

    return desconto

def insert(self, cliente_id, vendedor_id, forma_pagamento_id, produto_id, quantidade):
    if self.verificar_estoque(produto_id, quantidade):
        desconto = self.calcular_desconto(cliente_id)

        sql = "INSERT INTO Compra (cliente_id, vendedor_id, forma_pagamento_id, desconto) VALUES (%s, %s, %s, %s);"
        self.execute(sql, (cliente_id, vendedor_id, forma_pagamento_id, desconto))
        self.commit()

        # Atualize o estoque do produto
        sql = "UPDATE Produto SET estoque = estoque - %s WHERE id = %s;"
        self.execute(sql,(quantidade ,produto_id))
        
class ClienteForm(tk.Frame):
    def __init__(self,master=None):
       super().__init__(master)
       self.master=master
       self.pack()
       
       # Criação dos campos de entrada e botões para o formulário do cliente
       # Adicione aqui o código para criar os campos de entrada e botões para o formulário do cliente

def insert_cliente(nome,cpf ,sexo,email,cidade,timefutebol ,animefavorito ):
   try:
      conn=psycopg2.connect(
         dbname="dbproject",
         user="postgres",
         password="12345678",
         host="localhost"
      )
      cur=conn.cursor()
      
      # Execute a instrução SQL para inserir um novo cliente na tabela Cliente
      sql="INSERT INTO cliente (nome,cpf ,sexo,email,cidade,timefutebol ,animefavorito ) VALUES (%s,%s,%s,%s,%s,%s,%s);"
      cur.execute(sql,(nome,cpf ,sexo,email,cidade,timefutebol ,animefavorito ))
      
      conn.commit()
      cur.close()
      conn.close()
      print("Cliente inserido com sucesso!")
      
   except Exception as e:
      print("Erro ao inserir cliente:",str(e))

class FormaPagamentoForm(tk.Frame):
    def __init__(self,master=None):
       super().__init__(master)
       self.master=master
       self.pack()
       
       # Criação dos campos de entrada e botões para o formulário de forma de pagamento
       # Adicione aqui o código para criar os campos de entrada e botões para o formulário de forma de pagamento

def insert_forma_pagamento(tipo,status):
   try:
      conn=psycopg2.connect(
         dbname="dbproject",
         user="postgres",
         password="12345678",
         host="localhost"
      )
      cur=conn.cursor()
      
      # Execute a instrução SQL para inserir uma nova forma de pagamento na tabela FormaPagamento
      sql="INSERT INTO FormaPagamento (tipo,status) VALUES (%s,%s);"
      cur.execute(sql,(tipo,status))
      
      conn.commit()
      cur.close()
      conn.close()
      print("Forma de pagamento inserida com sucesso!")
      
   except Exception as e:
      print("Erro ao inserir forma de pagamento:",str(e))

class ProdutoForm(tk.Frame):
    def __init__(self,master=None):
       super().__init__(master)
       self.master=master
       self.pack()
       
       # Criação dos campos de entrada e botões para o formulário do produto
       # Adicione aqui o código para criar os campos de entrada e botões para o formulário do produto

def insert_produto(nome,preco,quantidade):
   try:
      conn=psycopg2.connect(
         dbname="dbproject",
         user="postgres",
         password="12345678",
         host="localhost"
      )
      cur=conn.cursor()
      
      # Execute a instrução SQL para inserir um novo produto na tabela Produto
      sql="INSERT INTO Produto (nome,preco,estoque) VALUES (%s,%s,%s);"
      cur.execute(sql,(nome,preco,quantidade))
      
      conn.commit()
      cur.close()
      conn.close()
      print("Produto inserido com sucesso!")
      
   except Exception as e:
      print("Erro ao inserir produto:",str(e))

class VendedorForm(tk.Frame):
    def __init__(self,master=None):
       super().__init__(master)
       self.master=master
       self.pack()
       
       # Criação dos campos de entrada e botões para o formulário do vendedor
       # Adicione aqui o código para criar os campos de entrada e botões para o formulário do vendedor

def insert_vendedor(nome,cpf ):
   try:
      conn=psycopg2.connect(
         dbname="dbproject",
         user="postgres",
         password="12345678",
         host="localhost"
      )
      cur=conn.cursor()
      
      # Execute a instrução SQL para inserir um novo vendedor na tabela Vendedor
      sql="INSERT INTO Vendedor (nome,cpf ) VALUES (%s,%s);"
      cur.execute(sql,(nome,cpf ))
      
      conn.commit()
      cur.close()
      conn.close()
      print("Vendedor inserido com sucesso!")
      
   except Exception as e:
      print("Erro ao inserir vendedor:",str(e))

class VisualizarProdutos(tk.Toplevel):
    def __init__(self,parent,connection):
        super().__init__(parent)
        self.parent=parent
        self.connection=connection
        self.title("Produtos Existentes")
        
        self.produtos_listbox=tk.Listbox(self,selectmode=tk.SINGLE)
        self.produtos_listbox.pack(fill=tk.BOTH,expand=True)
        
        self.carregar_produtos()

    def carregar_produtos(self):
        sql = "SELECT id,nome,preco,estoque FROM Produto;"
        self.connection.cur.execute(sql)
        produtos=self.connection.cur.fetchall()

        for produto in produtos:
            produto_info=f"ID: {produto[0]}, Nome: {produto[1]}, Preço: {produto[2]}, Estoque: {produto[3]}"
            self.produtos_listbox.insert(tk.END,produto_info)

def main():
    root = tk.Tk()
    connection = Connection()

    visualizar_produtos_button = tk.Button(root,text="Visualizar Produtos",command=lambda: VisualizarProdutos(root,connection))
    visualizar_produtos_button.pack()

    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    ClienteForm(root)
    FormaPagamentoForm(root)
    ProdutoForm(root)
    VendedorForm(root)