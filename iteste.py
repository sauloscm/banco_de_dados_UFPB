import tkinter as tk
import psycopg2
from tkinter import PhotoImage
from tkinter import ttk


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
        
class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")        
        
        
class ProdutoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Produtos")
        
        # Crie um contêiner para a árvore e a barra de rolagem
        container = ttk.Frame(root)
        container.pack(fill='both', expand=True)

        # Crie uma barra de rolagem vertical
        self.scrollbar = ttk.Scrollbar(container)
        self.scrollbar.pack(side='right', fill='y')

        # Crie a árvore
        self.tree = ttk.Treeview(container, columns=("Quantidade em Estoque", "Validade", "Fabricante", "Valor", "Marca", "Fabricado em Mari"), yscrollcommand=self.scrollbar.set)
        self.tree.heading("#1", text="Quantidade em Estoque")
        self.tree.heading("#2", text="Validade")
        self.tree.heading("#3", text="Fabricante")
        self.tree.heading("#4", text="Valor")
        self.tree.heading("#5", text="Marca")
        self.tree.heading("#6", text="Fabricado em Mari")
        self.tree.pack(side='left', fill='both', expand=True)

        # Conecte a barra de rolagem à árvore
        self.scrollbar.config(command=self.tree.yview)

        self.load_data()
        
        self.cadastro_button = tk.Button(root, text="Cadastro de Produto", command=self.show_cadastro)
        self.cadastro_button.pack()
    
    def load_data(self):
        try:
            conn = psycopg2.connect(
                dbname="dbproject",
                user="postgres",
                password="12345678",
                host="localhost"
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM produto")
            rows = cur.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
            
            conn.close()
        except Exception as e:
            print("Erro ao buscar dados:", str(e))
    
    def show_cadastro(self):
        self.root.withdraw()  # Esconder a janela atual
        cadastro_window = tk.Toplevel(self.root)
        cadastro_app = CadastroProdutoApp(cadastro_window, self)   
        
    
        
class CadastroProdutoApp:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        self.root.title("Cadastro de Produto")    
        
def show_produtos():
    root = tk.Tk()
    app = ProdutoApp(root)
    root.mainloop()            

class Compra(Connection):
    def insert(self, cliente_id, vendedor_id, forma_pagamento_id):
        try:
            # Certifique-se de que os IDs fornecidos existam no banco de dados
            if not self.check_id_exists("Cliente", cliente_id) or \
               not self.check_id_exists("Vendedor", vendedor_id) or \
               not self.check_id_exists("FormaPagamento", forma_pagamento_id):
                print("IDs inválidos. Verifique se os IDs existem no banco de dados.")
                return False

            sql = "INSERT INTO Compra (cliente_id, vendedor_id, forma_pagamento_id) VALUES (%s, %s, %s) RETURNING id;"
            self.execute(sql, (cliente_id, vendedor_id, forma_pagamento_id))
            compra_id = self.cur.fetchone()[0]
            self.commit()

            print(f"Compra registrada com sucesso! ID da compra: {compra_id}")
            return compra_id
        except Exception as e:
            print("Erro ao inserir compra:", str(e))
            return False

    def delete(self, compra_id):
        try:
            sql = "DELETE FROM Compra WHERE id = %s;"
            self.execute(sql, (compra_id,))
            self.commit()
            print(f"Compra ID {compra_id} deletada com sucesso.")
        except Exception as e:
            print(f"Erro ao deletar compra ID {compra_id}:", str(e))

    def update(self, compra_id, cliente_id, vendedor_id, forma_pagamento_id):
        try:
            # Certifique-se de que os IDs fornecidos existam no banco de dados
            if not self.check_id_exists("Cliente", cliente_id) or \
               not self.check_id_exists("Vendedor", vendedor_id) or \
               not self.check_id_exists("FormaPagamento", forma_pagamento_id):
                print("IDs inválidos. Verifique se os IDs existem no banco de dados.")
                return False

            sql = "UPDATE Compra SET cliente_id = %s, vendedor_id = %s, forma_pagamento_id = %s WHERE id = %s;"
            self.execute(sql, (cliente_id, vendedor_id, forma_pagamento_id, compra_id))
            self.commit()
            print(f"Compra ID {compra_id} atualizada com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar compra ID {compra_id}:", str(e))

    def search(self, compra_id):
        try:
            sql = "SELECT * FROM Compra WHERE id = %s;"
            self.execute(sql, (compra_id,))
            compra = self.cur.fetchone()
            if compra:
                print(f"Detalhes da compra ID {compra_id}:")
                print(f"Cliente ID: {compra[1]}")
                print(f"Vendedor ID: {compra[2]}")
                print(f"Forma de Pagamento ID: {compra[3]}")
            else:
                print(f"Compra ID {compra_id} não encontrada.")
        except Exception as e:
            print(f"Erro ao buscar compra ID {compra_id}:", str(e))


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
        self.execute(sql, (quantidade, produto_id))
        self.commit()

        return True
    else:
        return False  # Não foi possível efetivar a compra devido à falta de estoque

class ClienteForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()        

        self.nome_label = tk.Label(self, text="Nome")
        self.nome_label.pack()
        self.nome_entry = tk.Entry(self)
        self.nome_entry.pack()

        self.cpf_label = tk.Label(self, text="CPF")
        self.cpf_label.pack()
        self.cpf_entry = tk.Entry(self)
        self.cpf_entry.pack()

        self.sexo_label = tk.Label(self, text="Sexo")
        self.sexo_label.pack()
        self.sexo_entry = tk.Entry(self)
        self.sexo_entry.pack()

        self.email_label = tk.Label(self, text="Email")
        self.email_label.pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        self.cidade_label = tk.Label(self, text="Cidade")
        self.cidade_label.pack()
        self.cidade_entry = tk.Entry(self)
        self.cidade_entry.pack()

        self.timefutebol_label = tk.Label(self, text="Time de Futebol")
        self.timefutebol_label.pack()
        self.timefutebol_entry = tk.Entry(self)
        self.timefutebol_entry.pack()

        self.animefavorito_label = tk.Label(self, text="Anime Favorito")
        self.animefavorito_label.pack()
        self.animefavorito_entry = tk.Entry(self)
        self.animefavorito_entry.pack()

        self.submit_button = tk.Button(self)
        self.submit_button["text"] = "Submit"
        self.submit_button["command"] = self.submit
        self.submit_button.pack()       

    def submit(self):
        nome = self.nome_entry.get()
        cpf = self.cpf_entry.get()
        sexo = self.sexo_entry.get()
        email = self.email_entry.get()
        cidade = self.cidade_entry.get()
        timefutebol = self.timefutebol_entry.get()
        animefavorito = self.animefavorito_entry.get()

        insert_cliente(nome, cpf, sexo, email, cidade, timefutebol, animefavorito)  # Chama a função para inserir o cliente

        # Limpa os campos de entrada após a inserção
        self.nome_entry.delete(0, tk.END)
        self.cpf_entry.delete(0, tk.END)
        self.sexo_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.cidade_entry.delete(0, tk.END)
        self.timefutebol_entry.delete(0, tk.END)
        self.animefavorito_entry.delete(0, tk.END)


def insert_cliente(nome, cpf, sexo, email, cidade, timefutebol, animefavorito):
    try:
        conn = psycopg2.connect(
            dbname="dbproject",
            user="postgres",
            password="12345678",
            host="localhost"
        )
        cur = conn.cursor()

        # Execute a instrução SQL para inserir um novo cliente na tabela Cliente
        sql = "INSERT INTO cliente (nome, cpf, sexo, email, cidade, timefutebol, animefavorito) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cur.execute(sql, (nome, cpf, sexo, email, cidade, timefutebol, animefavorito))

        conn.commit()
        cur.close()
        conn.close()
        print("Cliente inserido com sucesso!")

    except Exception as e:
        print("Erro ao inserir cliente:", str(e))


class FormaPagamentoForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.tipo_label = tk.Label(self, text="Tipo de pagamento")
        self.tipo_label.pack()

        # Crie uma caixa de seleção (combobox) para escolher a forma de pagamento
        self.forma_pagamento_var = tk.StringVar()
        self.forma_pagamento_combobox = ttk.Combobox(self, textvariable=self.forma_pagamento_var, values=["Cartão", "Boleto", "PIX", "Berries"])
        self.forma_pagamento_combobox.set("Selecione uma forma de pagamento")
        self.forma_pagamento_combobox.pack()

        self.status_label = tk.Label(self, text="Status")
        self.status_label.pack()
        self.status_entry = tk.Entry(self)
        self.status_entry.pack()

        self.submit_button = tk.Button(self)
        self.submit_button["text"] = "Submit"
        self.submit_button["command"] = self.submit
        self.submit_button.pack()

    def submit(self):
        forma_pagamento = self.forma_pagamento_var.get()
        status_pagamento = self.status_entry.get()

        # Verifique se a forma de pagamento foi selecionada corretamente
        if forma_pagamento == "Selecione uma forma de pagamento":
            print("Selecione uma forma de pagamento válida.")
            return

        # Solicite o status de pagamento usando um diálogo
        if status_pagamento:
            # Chame a função para inserir a forma de pagamento com a forma_pagamento e status_pagamento
            insert_forma_pagamento(forma_pagamento, status_pagamento)

        # Limpe os campos de entrada após a inserção
        self.forma_pagamento_combobox.set("Selecione uma forma de pagamento")
        self.status_entry.delete(0, tk.END)

def insert_forma_pagamento(tipo, status):
    try:
        conn = psycopg2.connect(
            dbname="dbproject",
            user="postgres",
            password="12345678",
            host="localhost"
        )
        cur = conn.cursor()
        
        # Execute a instrução SQL para inserir uma nova forma de pagamento na tabela FormaPagamento
        sql = "INSERT INTO FormaPagamento (tipo, status) VALUES (%s, %s);"
        cur.execute(sql, (tipo, status))
        
        conn.commit()
        cur.close()
        conn.close()
        print("Forma de pagamento inserida com sucesso!")

    except Exception as e:
        print("Erro ao inserir forma de pagamento:", str(e))


class ProdutoForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # Adicione elementos de interface para os filtros restantes (categoria e origem)
        self.categoria_label = tk.Label(self, text="Filtrar por Categoria")
        self.categoria_label.pack()
        self.categoria_entry = tk.Entry(self)
        self.categoria_entry.pack()

        self.origem_label = tk.Label(self, text="Filtrar por Origem (Mari)")
        self.origem_label.pack()
        self.origem_var = tk.BooleanVar()
        self.origem_checkbox = tk.Checkbutton(self, text="Fabricado em Mari", variable=self.origem_var)
        self.origem_checkbox.pack()

        self.nome_label = tk.Label(self, text="Nome")
        self.nome_label.pack()
        self.nome_entry = tk.Entry(self)
        self.nome_entry.pack()

        self.buscar_button = tk.Button(self)
        self.buscar_button["text"] = "Buscar Produtos"
        self.buscar_button["command"] = self.buscar_produtos
        self.buscar_button.pack()

    def buscar_produtos(self):
        nome_filtro = self.nome_entry.get()
        categoria_filtro = self.categoria_entry.get()
        origem_filtro = self.origem_var.get()

        # Adicione aqui a lógica para construir a consulta SQL com base nos filtros selecionados

        # Exemplo de consulta SQL (não esqueça de adaptá-la às suas tabelas e campos):
        sql = "SELECT * FROM Produto WHERE 1=1"
        args = []

        if nome_filtro:
            sql += " AND nome ILIKE %s"
            args.append(f"%{nome_filtro}%")

        if categoria_filtro:
            sql += " AND categoria ILIKE %s"
            args.append(f"%{categoria_filtro}%")

        if origem_filtro:
            sql += " AND origem = true"

        # Execute a consulta e exiba os resultados (você pode mostrar os resultados em uma janela ou console)

        # Limpe os campos de filtro após a pesquisa
        self.nome_entry.delete(0, tk.END)
        self.categoria_entry.delete(0, tk.END)

def insert_produto(nome, preco, quantidade):
    try:
        conn = psycopg2.connect(
            dbname="dbproject",
            user="postgres",
            password="12345678",
            host="localhost"
        )
        cur = conn.cursor()
        
        # Execute a instrução SQL para inserir um novo produto na tabela Produto
        sql = "INSERT INTO Produto (nome, preco, estoque) VALUES (%s, %s, %s);"
        cur.execute(sql, (nome, preco, quantidade))
        
        conn.commit()
        cur.close()
        conn.close()
        print("Produto inserido com sucesso!")

    except Exception as e:
        print("Erro ao inserir produto:", str(e))

class VendedorForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.nome_label = tk.Label(self, text="Nome Vendedor")
        self.nome_label.pack()
        self.nome_entry = tk.Entry(self)
        self.nome_entry.pack()

        self.cpf_label = tk.Label(self, text="CPF")
        self.cpf_label.pack()
        self.cpf_entry = tk.Entry(self)
        self.cpf_entry.pack()

        self.submit_button = tk.Button(self)
        self.submit_button["text"] = "Submit"
        self.submit_button["command"] = self.submit
        self.submit_button.pack()

    def submit(self):
        nome = self.nome_entry.get()
        cpf = self.cpf_entry.get()

        # Adicione aqui o código para inserir o novo vendedor no banco de dados
        insert_vendedor(nome, cpf)  # Chama a função para inserir o vendedor

        # Limpa os campos de entrada após a inserção
        self.nome_entry.delete(0, tk.END)
        self.cpf_entry.delete(0, tk.END)

def insert_vendedor(nome, cpf):
    try:
        conn = psycopg2.connect(
            dbname="dbproject",
            user="postgres",
            password="12345678",
            host="localhost"
        )
        cur = conn.cursor()
        
        # Execute a instrução SQL para inserir um novo vendedor na tabela Vendedor
        sql = "INSERT INTO Vendedor (nome, cpf) VALUES (%s, %s);"
        cur.execute(sql, (nome, cpf))
        
        conn.commit()
        cur.close()
        conn.close()
        print("Vendedor inserido com sucesso!")

    except Exception as e:
        print("Erro ao inserir vendedor:", str(e))
        
        
class VisualizarProdutos(tk.Toplevel):
    def __init__(self, parent, connection):
        super().__init__(parent)
        self.parent = parent
        self.connection = connection
        self.title("Produtos Existentes")
        
        self.produtos_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.produtos_listbox.pack(fill=tk.BOTH, expand=True)
        
        self.carregar_produtos()
    
    def carregar_produtos(self):
        sql = "SELECT id, nome, preco, estoque FROM Produto;"
        self.connection.cur.execute(sql)
        produtos = self.connection.cur.fetchall()
        
        for produto in produtos:
            produto_info = f"ID: {produto[0]}, Nome: {produto[1]}, Preço: {produto[2]}, Estoque: {produto[3]}"
            self.produtos_listbox.insert(tk.END, produto_info)
            
    
    


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # Carregar a imagem do carrinho de compras
        self.cart_image = PhotoImage(file="carrinho.png")

        # Criar o botão do carrinho de compras
        self.cart_button = tk.Button(self, image=self.cart_image, command=self.view_cart)
        self.cart_button.pack()

        # Inicializar o carrinho como uma lista vazia
        self.cart = []

    def view_cart(self):
        # Criar uma nova janela para visualizar o carrinho
        self.cart_window = tk.Toplevel(self)
        self.cart_window.title("Carrinho de Compras")

        # Adicionar os itens do carrinho à janela
        for item in self.cart:
            label = tk.Label(self.cart_window, text=item)
            label.pack()

    def add_to_cart(self, item):
        # Adicionar um item ao carrinho
        self.cart.append(item)
          



    
    
if __name__ == "__main__":
    root = tk.Tk()
    app = ProdutoApp(root)
    ClienteForm(root)
    FormaPagamentoForm(root)
    ProdutoForm(root)
    VendedorForm(root)  # Adicione esta linha
    root.mainloop()
    app = Application(master=root)
    frame = ScrollableFrame(root)
    frame.pack(fill='both', expand=True)
    
    
    
    
    
