import pandas as pd
import re
from dateutil.parser import parse
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import requests
from datetime import datetime

# Caminho para a credencial da conta de serviço
CREDENTIALS_PATH = 'credentials/people-analytics-pipoca-agil-google-drive.json'

# Configuração da autenticação com conta de serviço
class GoogleDriveManager:
    def __init__(self):
        self.authenticate()

    def authenticate(self):
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=[
            'https://www.googleapis.com/auth/drive'
        ])
        self.service = build('drive', 'v3', credentials=creds)

    def get_file_by_name(self, folder_id_origem, file_name):
        query = f"'{folder_id_origem}' in parents and name = '{file_name}' and trashed = false"
        #print(f"Query: {query}")
        result = self.service.files().list(q=query).execute().get('files', [])
        #print(f"Result: {result}")
        return result[0] if result else None

    def download_excel(self, file_id):
        request = self.service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        file_stream.seek(0)
        return file_stream

    def upload_file(self, folder_id_origem, file_name, file_path):
        file_metadata = {'name': file_name, 'parents': [folder_id_origem]}
        media = MediaFileUpload(file_path, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file['id']

# Extração de dados
class DataExtractor:
    def __init__(self, drive_manager, folder_id_origem, file_name):
        self.drive_manager = drive_manager
        self.folder_id_origem = folder_id_origem
        self.file_name = file_name

    def load_excelfile(self):
        file_data = self.drive_manager.get_file_by_name(self.folder_id_origem, self.file_name)
        if not file_data:
            raise FileNotFoundError("Arquivo não encontrado no Google Drive")
        file_stream = self.drive_manager.download_excel(file_data['id'])
        return pd.read_excel(file_stream, header=None)

# Transformação de dados
class DataTransformer:
    def __init__(self, df_raw):
        self.df_raw = df_raw
    
    def retirar_acento(self, frase):
        nova = frase.lower()
        nova = re.sub(r'[àáâãäå]', 'a', nova)
        nova = re.sub(r'[èéêë]', 'e', nova)
        nova = re.sub(r'[ìíîï]', 'i', nova)
        nova = re.sub(r'[òóôõö]', 'o', nova)
        nova = re.sub(r'[ùúûü]', 'u', nova)
        nova = re.sub(r'ç', 'c', nova)
        return nova
    
    def normalizar_perguntas(self, pergunta):
        fase1 = pergunta.split('.')[1].lstrip()
        fase2 = re.sub(r'[^\w\s]', '', fase1)
        fase3 = self.retirar_acento(fase2)
        fase4 = re.sub(' ', '_', fase3)
        return fase4
    
    def verificar_email(self, email):
        padraoEmail = r'^[\w\-.]+@[\w-]+\.[a-zA-Z]{2,}$'
        return "Pass" if re.match(padraoEmail, email) else "Email Incorreto"
    
    def padronizar_datastring(self,dataStamp): 
        try:
        # Attempt to parse the string into a datetime object
          parsed_date = parse(str(dataStamp))
          return parsed_date.strftime("%d-%m-%Y %H:%M:%S")
        except (ValueError, TypeError):
        # Return a default value or handle invalid input gracefully
          return "Invalid Date"
    
    def renomear_colunas_autoavaliacao(self):
        colunas = ['timestamp', 'emailRespondente', 'nomeRespondente', 'funcaoDesempenha', 'equipeParticipante']
        self.df_raw.columns = colunas + [f'pergunta_{i}' for i in range(len(self.df_raw.columns) - len(colunas))]
    
    def validar_email(self):
        self.df_raw['emailRespondente'] = self.df_raw['emailRespondente'].apply(lambda x: x if self.verificar_email(x) == 'Pass' else None)
    
    def transformar_dados(self):
        self.renomear_colunas_autoavaliacao()
        self.validar_email()
        self.df_raw['timestamp'] = self.df_raw['timestamp'].apply(self.padronizar_datastring)
        return self.df_raw    

# Processo principal
def processar_arquivo(folder_id_origem, folder_id_destino, file_name):
    drive_manager = GoogleDriveManager()
    extractor = DataExtractor(drive_manager, folder_id_origem, file_name)
    df = extractor.load_excelfile()
    transformer = DataTransformer(df)
    df_transformado = transformer.transformar_dados()
    file_path = f"{file_name}_processado.xlsx"
    df_transformado.to_excel(file_path, index=False)
    drive_manager.upload_file(folder_id_destino, file_path, file_path)
    print("Arquivo processado e salvo no Google Drive.")

# IDs das pastas
folder_id_origem = "1E6AEUGqRp3IJsWV4qAwMRJK_tMD7wDYT" #pasta people_analytics/raw/
folder_id_destino = "1WJlq1C_uLq9J3Ta-lVAkQVv7AzblftsD" #pasta people_analytics/trusted/
file_name = "autoavalicao_pipoca.xlsx"

# Executar o processamento
processar_arquivo(folder_id_origem, folder_id_destino, file_name)
