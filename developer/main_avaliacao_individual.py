from notificacao_discord import DiscordNotifier
from datetime import datetime
from leitura_arquivo_drive import GoogleAuthenticator, GoogleDriveManager, GoogleSheetsManager
from transformacao_avaliacao_individual_fato_respostas import processar_arquivo, processar_fato_respostas, TransformerFatoRespostas
import pandas as pd

# Definições iniciais
relatorio = 'avaliacao_individual'  # Opções: autoavaliacao, avaliacao_coletiva, avaliacao_projeto, #avaliacao_individual
camada = 'raw'
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
relatorio_raw = "avaliacao_individual.xlsx"
file_name = "avaliacao_individual.xlsx"
relatorio_final = 'fato_respostas'

# Instancia a classe de comunicação com o Discord
notifier = DiscordNotifier()
notifier.enviar_notificacao(f"{timestamp} - Início do processo de transformação de dados.", processo=relatorio, status="sucesso")

# Autenticar no Google Drive
auth = GoogleAuthenticator()
drive_service = auth.drive_service  # Obter o serviço de drive autenticado
drive_manager = GoogleDriveManager(drive_service)  # Passar o serviço de drive para o construtor

try:
    # Transformação do raw para trusted
    processar_arquivo(drive_manager, file_name, relatorio)
    
    # Carregar os dados transformados
    df_trusted = pd.read_excel(f"{relatorio}_processado.xlsx")
    transformer = TransformerFatoRespostas(df_trusted,file_name)
    
    # Transformação do trusted para refined (modelo fato_respostas)
    processar_fato_respostas(drive_manager, transformer, relatorio_final)
    
    notifier.enviar_notificacao(f"{timestamp} - Transformação de dados concluída com sucesso.", processo=relatorio, status="sucesso")

except Exception as e:
    notifier.enviar_notificacao(f"{timestamp} - Erro durante o processo de transformação: {str(e)}", processo=relatorio, status="falha")
    raise e