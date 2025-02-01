import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
import pandas as pd
import logging
import os

class GoogleAuthenticator:
    """Gerencia a autenticação do Google Sheets e Google Drive."""

    def __init__(self):
        """
        Inicializa a autenticação com as credenciais fornecidas.

        Args:
            credentials_path (str): Caminho do arquivo JSON de credenciais.
        """
        self.sheets_client = None
        self.drive_service = None
        self.authenticate()

    def authenticate(self):
        """Autentica na API do Google Sheets e Google Drive."""
        try:
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            # credencial para acessar o Google Drive
            credentials_path = 'credentials/people-analytics-pipoca-agil-google-drive.json'

            credentials = Credentials.from_service_account_file(credentials_path, scopes=scopes)

            # Cliente para Google Sheets
            self.sheets_client = gspread.authorize(credentials)

            # Cliente para Google Drive
            self.drive_service = build('drive', 'v3', credentials=credentials)

            logging.info("Autenticação bem-sucedida no Google Sheets e Google Drive.")
        except Exception as e:
            logging.error(f"Erro na autenticação: {e}")
            raise

class GoogleSheetsManager:
    """Gerencia operações com o Google Sheets."""

    def __init__(self, client):
        """
        Inicializa o gerenciador do Google Sheets.

        Args:
            client (gspread.Client): Cliente autenticado do Google Sheets.
        """
        self.client = client
        self.sheet_ids = {
            'autoavaliacao': '1NmhI61q2bZJBWr3Vb3C_Y6siGUOC1rk66FOXu3gUN00',
            'avaliacao_individual': '1CNhr4wFnrqLuHfU0LUm2SQV4RtF8EAECaRgSQhTvxyY',
            'avaliacao_coletiva': '1tOuJ95zjUiyHQCwY5gMF9uSVnbAr5Fwy-OMWTe_WTpo',
            'avaliacao_projeto': '1FpDuXzn7HIeDh5ZCHxUVtiQGBY3XiQ_v196z56MuHag'
        }

    def get_sheet(self, relatorio):
        """Obtém a planilha pelo ID correspondente ao relatório."""
        if relatorio not in self.sheet_ids:
            logging.error(f"Erro ao acessar a planilha: Relatório '{relatorio}' inválido.")
            raise ValueError(f"Relatório '{relatorio}' não encontrado.")

        sheet_id = self.sheet_ids[relatorio]

        try:
            sheet = self.client.open_by_key(sheet_id).sheet1
            logging.info(f"Conectado à planilha ID: {sheet_id}")
            return sheet
        except Exception as e:
            logging.error(f"Erro ao acessar a planilha: {e}")
            raise

    def get_data(self, sheet):
        """Obtém todos os dados da planilha e retorna como lista de listas."""
        try:
            data = sheet.get_all_values()
            logging.info("Dados obtidos com sucesso da planilha.")
            return data
        except Exception as e:
            logging.error(f"Erro ao obter dados da planilha: {e}")
            raise

class GoogleDriveManager:
    """Gerencia operações de upload de arquivos no Google Drive."""

    def __init__(self, drive_service, folder_id):
        """
        Inicializa o gerenciador do Google Drive.

        Args:
            drive_service: Cliente autenticado do Google Drive.
            folder_id (str): ID da pasta no Google Drive onde os arquivos serão armazenados.
        """
        self.drive_service = drive_service
        self.folder_id = folder_id

    def save_data_to_excel_and_upload(self, data):
        """Salva os dados em um arquivo Excel local e faz upload para o Google Drive."""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            file_name = f"autoavaliacao_pipoca_{timestamp}.xlsx"

            # Criar DataFrame e salvar como arquivo Excel
            df = pd.DataFrame(data)
            df.to_excel(file_name, index=False, header=False)

            logging.info("Arquivo Excel gerado com sucesso.")

            # Upload para o Google Drive
            file_metadata = {
                'name': file_name,
                'parents': [self.folder_id]
            }
            media = MediaFileUpload(file_name, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            logging.info(f"Arquivo enviado para o Google Drive com sucesso. ID: {file.get('id')}")

            # Remover arquivo local após o upload
            os.remove(file_name)

        except Exception as e:
            logging.error(f"Erro ao salvar o arquivo no Google Drive: {e}")
            raise

def setup_logging():
    """Configura o logging para registrar informações e erros."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

if __name__ == "__main__":
    setup_logging()

    folder_id = '1E6AEUGqRp3IJsWV4qAwMRJK_tMD7wDYT' #Pasta people_analytics/RAW
    auth = GoogleAuthenticator()
    sheets_manager = GoogleSheetsManager(auth.sheets_client, sheet_id)
    drive_manager = GoogleDriveManager(auth.drive_service, folder_id)

    data = sheets_manager.get_data()
    drive_manager.save_data_to_excel_and_upload(data)
