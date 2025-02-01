# Importando as classes desenvolvidas anteriormente
from notificacao_discord import DiscordNotifier
from datetime import datetime
from leitura_arquivo_drive import GoogleAuthenticator, GoogleSheetsManager, GoogleDriveManager
from transformacao_autoavaliacao import *

# Defina qual relatório você deseja integrar os dados
relatorio = 'avaliacao_coletiva'  # Opções: autoavaliacao, avaliacao_coletiva, avaliacao_projeto

# defina qual camada você deseja salvar o arquivo em excel
camada = 'raw'

# Define a timestamp
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Instancia a classe de comunicação com o Discord
notifier = DiscordNotifier()

# Notificar início do processo
notifier.enviar_notificacao(f"{timestamp} - A transformação de dados foi iniciada.", processo=f'{relatorio}', status="sucesso")

# Autenticar no Google Drive e Google Sheets
auth = GoogleAuthenticator()
sheets_manager = GoogleSheetsManager(auth.sheets_client) 
drive_manager = GoogleDriveManager(auth.drive_service, camada)

# Obter a planilha correspondente ao relatório
sheet = sheets_manager.get_sheet(relatorio)

# Ler dados da planilha
data = sheets_manager.get_data(sheet)

# Gerar um Excel e enviar para a pasta people_analytics/[camada] do Google Drive
drive_manager.save_data_to_excel_and_upload(data, camada, relatorio)

# Notificar fim do processo
notifier.enviar_notificacao(f"{timestamp} - A transformação de dados foi concluída.", processo=f'{relatorio}', status="sucesso")
