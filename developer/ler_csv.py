import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


url = "https://docs.google.com/spreadsheets/d/1CNhr4wFnrqLuHfU0LUm2SQV4RtF8EAECaRgSQhTvxyY/gviz/tq?tqx=out:csv"

# Carregar os dados do Google Forms (por exemplo, de um arquivo CSV)
# Substitua 'respostas.csv' pelo caminho do seu arquivo exportado
fato_respostas = pd.read_csv(url)

print(fato_respostas)

# 1. Renomear colunas para um formato padronizado (exemplo: snake_case)
fato_respostas.columns = (
    fato_respostas.columns.str.strip()  # Remover espaços em excesso
    .str.lower()  # Transformar em minúsculas
    .str.replace(" ", "_")  # Substituir espaços por "_"
    .str.replace("[^a-z0-9_]", "", regex=True)  # Remover caracteres especiais
)

# 2. Padronizar formatos de dados
# Exemplo: Converter datas para formato ISO (YYYY-MM-DD)
if 'data' in fato_respostas.columns:
    fato_respostas['data'] = pd.to_datetime(fato_respostas['data'], errors='coerce').dt.strftime('%Y-%m-%d')

# Exemplo: Normalizar texto (remover espaços, colocar em maiúsculas)
if 'nome' in fato_respostas.columns:
    fato_respostas['nome'] = fato_respostas['nome'].str.strip().str.title()

# Exemplo: Padronizar valores numéricos
if 'idade' in fato_respostas.columns:
    fato_respostas['idade'] = pd.to_numeric(fato_respostas['idade'], errors='coerce').fillna(0).astype(int)

# 3. Preencher valores ausentes ou substituir por padrões
fato_respostas.fillna({
    'email': 'não informado',  # Exemplo: Preencher emails ausentes
    'idade': 0,  # Exemplo: Idade padrão como 0
}, inplace=True)

# 4. Validar e corrigir valores inconsistentes
# Exemplo: Garantir que emails tenham o formato correto
if 'email' in fato_respostas.columns:
    fato_respostas['email'] = fato_respostas['email'].str.strip().str.lower()
    fato_respostas['email_valido'] = fato_respostas['email'].str.contains(r'^[\w\.-]+@[\w\.-]+\.\w+$', na=False)

# 5. Salvar os dados padronizados em um novo arquivo (se necessário)
fato_respostas.to_csv("fato_respostas_padronizado.csv", index=False)

print("Dados padronizados salvos em 'fato_respostas_padronizado.csv'")
