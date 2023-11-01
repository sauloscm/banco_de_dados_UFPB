import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

class ProductApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.products = [Product("Produto A", 100.0, 5), Product("Produto B", 50.0, 3)]
        self.create_widgets()
        self.cliente_nome = None
        self.cliente_cpf = None
        self.pedidos_realizados = []
        self.forma_pagamento = None
        self.status_pagamento = None

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack()

        self.tab_comprar = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_comprar, text="Comprar Produto")
        self.create_comprar_tab()

        self.tab_dados_cadastrais = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_dados_cadastrais, text="Dados Cadastrais")
        self.create_dados_cadastrais_tab()

        self.tab_pedidos_realizados = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_pedidos_realizados, text="Pedidos Realizados")
        self.create_pedidos_realizados_tab()

    def create_comprar_tab(self):
        self.product_treeview = ttk.Treeview(self.tab_comprar, columns=("name", "price", "stock"), show="headings")
        self.product_treeview.heading("name", text="Nome")
        self.product_treeview.heading("price", text="Preço")
        self.product_treeview.heading("stock", text="Estoque")

        for product in self.products:
            self.product_treeview.insert("", "end", values=(product.name, f"R${product.price:.2f}", product.stock))

        self.product_treeview.pack()

        self.comprar_button = tk.Button(self.tab_comprar)
        self.comprar_button["text"] = "Comprar Produto"
        self.comprar_button["command"] = self.solicitar_informacoes_cliente
        self.comprar_button.pack()

        # Opções de forma de pagamento
        self.forma_pagamento_label = tk.Label(self.tab_comprar, text="Forma de Pagamento:")
        self.forma_pagamento_label.pack()
        self.forma_pagamento_var = tk.StringVar(self.tab_comprar)
        formas_pagamento = ["Selecione uma forma de pagamento", "Cartão", "Boleto", "PIX", "Berries"]
        self.forma_pagamento_var.set(formas_pagamento[0])
        self.forma_pagamento_menu = tk.OptionMenu(self.tab_comprar, self.forma_pagamento_var, *formas_pagamento)
        self.forma_pagamento_menu.pack()

    def create_dados_cadastrais_tab(self):
        self.dados_cadastrais_label = tk.Label(self.tab_dados_cadastrais, text="Dados Cadastrais do Cliente")
        self.dados_cadastrais_label.pack()

        self.nome_cliente_label = tk.Label(self.tab_dados_cadastrais, text="Nome:")
        self.nome_cliente_label.pack()
        
        self.cpf_cliente_label = tk.Label(self.tab_dados_cadastrais, text="CPF:")
        self.cpf_cliente_label.pack()

        self.atualizar_dados_button = tk.Button(self.tab_dados_cadastrais)
        self.atualizar_dados_button["text"] = "Atualizar Dados"
        self.atualizar_dados_button["command"] = self.atualizar_dados_cadastrais
        self.atualizar_dados_button.pack()

        self.dados_cadastrais_text = tk.Text(self.tab_dados_cadastrais, height=5, width=40)
        self.dados_cadastrais_text.pack()
        self.dados_cadastrais_text.configure(state="disabled")

    def create_pedidos_realizados_tab(self):
        self.pedidos_label = tk.Label(self.tab_pedidos_realizados, text="Pedidos Realizados")
        self.pedidos_label.pack()

        self.pedidos_text = tk.Text(self.tab_pedidos_realizados, height=10, width=40)
        self.pedidos_text.pack()
        self.pedidos_text.configure(state="disabled")

    def solicitar_informacoes_cliente(self):
        selected_item = self.product_treeview.selection()
        forma_pagamento = self.forma_pagamento_var.get()
        
        if selected_item and forma_pagamento != "Selecione uma forma de pagamento":
            item = self.product_treeview.item(selected_item)
            product_name = item["values"][0]
            product = next((p for p in self.products if p.name == product_name), None)

            if product and product.stock > 0:
                nome_cliente = self.obter_nome_cliente()
                cpf_cliente = self.obter_cpf_cliente()
                
                if nome_cliente and cpf_cliente:
                    resposta = messagebox.askokcancel("Comprar Produto", f"Você está comprando:\n\n{product_name}\nNome do Cliente: {nome_cliente}\nCPF: {cpf_cliente}\nForma de Pagamento: {forma_pagamento}\n\nConfirmar compra?")
                    if resposta:
                        # Pode prosseguir com a compra
                        self.status_pagamento = None  # Resetar o status de pagamento
                        if forma_pagamento != "Boleto":
                            self.status_pagamento = self.obter_status_pagamento(forma_pagamento)
                        
                        self.concluir_compra(product, nome_cliente, cpf_cliente, forma_pagamento, self.status_pagamento)
                        product.stock -= 1
                        messagebox.showinfo("Compra Realizada", f"Compra realizada com sucesso.\nProduto: {product_name}\nNome do Cliente: {nome_cliente}\nCPF: {cpf_cliente}\nForma de Pagamento: {forma_pagamento}")
            else:
                messagebox.showerror("Estoque Esgotado", "Desculpe, o produto selecionado não está disponível no momento.")
        else:
            messagebox.showerror("Seleção Inválida", "Selecione um produto e uma forma de pagamento válida para prosseguir.")

    def obter_nome_cliente(self):
        nome_cliente = simpledialog.askstring("Nome do Cliente", "Digite o nome do cliente:")
        if nome_cliente:
            self.cliente_nome = nome_cliente
            return nome_cliente
        return None

    def obter_cpf_cliente(self):
        cpf_cliente = simpledialog.askstring("CPF do Cliente", "Digite o CPF do cliente:")
        if cpf_cliente:
            self.cliente_cpf = cpf_cliente
            return cpf_cliente
        return None

    def obter_status_pagamento(self, forma_pagamento):
        if forma_pagamento != "Selecione uma forma de pagamento":
            if forma_pagamento == "Cartão":
                status_pagamento = simpledialog.askstring("Status de Pagamento", "Digite o status de pagamento (Aprovado, Rejeitado, Pendente):")
                return status_pagamento
            elif forma_pagamento == "PIX":
                status_pagamento = simpledialog.askstring("Status de Pagamento", "Digite o status de pagamento (Concluído, Pendente, Falhou):")
                return status_pagamento
            elif forma_pagamento == "Berries":
                status_pagamento = simpledialog.askstring("Status de Pagamento", "Digite o status de pagamento (OK, Insuficiente, Outro):")
                return status_pagamento
        return None

    def concluir_compra(self, product, nome_cliente, cpf_cliente, forma_pagamento, status_pagamento):
        pedido = f"Produto: {product.name} - R${product.price:.2f}\nNome do Cliente: {nome_cliente}\nCPF: {cpf_cliente}\nForma de Pagamento: {forma_pagamento}"
        if status_pagamento:
            pedido += f"\nStatus de Pagamento: {status_pagamento}"
        self.pedidos_realizados.append(pedido)

        # Atualize a guia de pedidos realizados
        self.pedidos_text.configure(state="normal")
        self.pedidos_text.delete("1.0", tk.END)
        for pedido in self.pedidos_realizados:
            self.pedidos_text.insert(tk.END, f"{pedido}\n\n")
        self.pedidos_text.configure(state="disabled")

    def atualizar_dados_cadastrais(self):
        nome_cliente = self.obter_nome_cliente()
        cpf_cliente = self.obter_cpf_cliente()
        dados_cadastrais = f"Nome do Cliente: {nome_cliente}\nCPF: {cpf_cliente}"

        # Atualize a guia de dados cadastrais
        self.dados_cadastrais_text.configure(state="normal")
        self.dados_cadastrais_text.delete("1.0", tk.END)
        self.dados_cadastrais_text.insert(tk.END, dados_cadastrais)
        self.dados_cadastrais_text.configure(state="disabled")

root = tk.Tk()
app = ProductApplication(master=root)
app.master.title("Loja Virtual")
app.mainloop()
