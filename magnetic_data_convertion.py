import os
import pandas as pd

# Definir caminho dos arquivos e colunas selecionadas
caminho_dos_arquivos = 'C:/Users/calaz/Documents/[4] CBPF 2023/Medidas dynacool/Junho/Dados'
colunas_selecionadas = ["Temperature (K)", "Magnetic Field (Oe)", "Moment (emu)"]

# Percorrer todos os arquivos do diretório
for nome_arquivo in os.listdir(caminho_dos_arquivos):
    # Verificar se é um arquivo .dat
    if nome_arquivo.endswith('.dat') or nome_arquivo.endswith('.DAT'):
        # Ler o arquivo
        df = pd.read_csv(os.path.join(caminho_dos_arquivos, nome_arquivo), delimiter=',', skiprows=35)
        # Selecionar as colunas desejadas
        df_selecionado = df.iloc[:, [2, 3, 4]]
        # Criar um novo arquivo com as colunas selecionadas
        nome_arquivo_novo = os.path.splitext(nome_arquivo)[0] + '_selecionado.txt'
        caminho_arquivo_novo = os.path.join(caminho_dos_arquivos, nome_arquivo_novo)
        df_selecionado.to_csv(caminho_arquivo_novo, sep='\t', index=False)
        print('Arquivo processado:', nome_arquivo)
        print('Arquivo exportado:', nome_arquivo_novo)
