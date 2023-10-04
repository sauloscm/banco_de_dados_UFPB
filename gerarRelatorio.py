def gerar_relatorio(table, nome_arquivo):
    
    resultado = table.list_all()
    try:
        with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
            writer = csv.writer(arquivo_csv)

            for row in resultado:
                writer.writerow([row[0], row[1], row[2], row[3], row[4]])

        print(f"Relatório exportado para {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")

def menu_gerar_relatorio(table):
     
    nome_arquivo = input("Digite o nome do arquivo CSV para exportar: ")
    gerar_relatorio(table, nome_arquivo)  # Chamada da função para exportar o relatório
