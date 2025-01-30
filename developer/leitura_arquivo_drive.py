import gspread
from google.oauth2.service_account import Credentials
import logging

def setup_logging():
    """Configura o logging para registrar informações e erros."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

def authenticate_google_sheets(credentials_path: str) -> gspread.Client:
    """Autentica na API do Google Sheets usando credenciais da conta de serviço."""
    try:
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        client = gspread.authorize(credentials)
        logging.info("Autenticação bem-sucedida no Google Sheets.")
        return client
    except Exception as e:
        logging.error(f"Erro na autenticação: {e}")
        raise

def get_google_sheet(client: gspread.Client, sheet_id: str):
    try:
        sheet = client.open_by_key(sheet_id).sheet1
        logging.info(f"Conectado à planilha ID: {sheet_id}")
        return sheet
    except Exception as e:
        logging.error(f"Erro ao acessar a planilha: {e}")
        raise

def get_sheet_data(sheet):
    """Obtém todos os dados da planilha e retorna como lista de listas."""
    try:
        data = sheet.get_all_values()
        logging.info("Dados obtidos com sucesso da planilha.")
        return data
    except Exception as e:
        logging.error(f"Erro ao obter dados da planilha: {e}")
        raise

def main():
    setup_logging()
    credentials_path = 'credentials\people-analytics-pipoca-agil-google-drive.json'  # Atualize com o caminho correto
    sheet_id = '1FpDuXzn7HIeDh5ZCHxUVtiQGBY3XiQ_v196z56MuHag'  # Substitua pelo caminho da sua planilha
    
    client = authenticate_google_sheets(credentials_path)
    sheet = get_google_sheet(client, sheet_id)
    data = get_sheet_data(sheet)
    
    for row in data:
        print(row)

if __name__ == "__main__":
    main()
