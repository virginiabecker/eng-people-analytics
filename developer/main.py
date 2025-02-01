# Importando as classes desenvolvidas anteriormente
from notificacao_discord import DiscordNotifier
from datetime import datetime
from leitura_arquivo_drive import GoogleAuthenticator, GoogleSheetsManager, GoogleDriveManager

# Defina qual relatório você deseja integrar os dados
relatorio = 'avaliacao_individual'  # Opções: autoavaliacao, avaliacao_coletiva, avaliacao_projeto

# Define a timestamp
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Parametrizar variáveis para comunicação com o Discord
URL_WEBHOOK = "https://discord.com/api/webhooks/1333091809139621939/aMNr3JAmrpzklttIUStqdp8W2BNPU91GNRzHPaPe3NjBiqHs69vVqbyw34I_FY0Aaf01"
notifier = DiscordNotifier(URL_WEBHOOK)

# Parametrizar variáveis para autenticação no Google
#credentials_path = 'credentials/people-analytics-pipoca-agil-google-drive.json'
folder_id = '1E6AEUGqRp3IJsWV4qAwMRJK_tMD7wDYT'

# Notificar início do processo
notifier.enviar_notificacao(f"{timestamp} - A transformação de dados foi iniciada.", processo=f'{relatorio}', status="sucesso")

# Autenticar no Google Drive e Google Sheets
auth = GoogleAuthenticator()
sheets_manager = GoogleSheetsManager(auth.sheets_client)  # Agora sem sheet_id
drive_manager = GoogleDriveManager(auth.drive_service, folder_id)

# Obter a planilha correspondente ao relatório
sheet = sheets_manager.get_sheet(relatorio)

# Ler dados da planilha
data = sheets_manager.get_data(sheet)

# Gerar um Excel e enviar para a pasta people_analytics/RAW do Google Drive
drive_manager.save_data_to_excel_and_upload(data)

# Notificar fim do processo
notifier.enviar_notificacao(f"{timestamp} - A transformação de dados foi concluída.", processo=f'{relatorio}', status="sucesso")
