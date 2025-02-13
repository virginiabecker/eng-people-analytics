import pandas as pd
import re
from dateutil.parser import parse
import io
import requests
from datetime import datetime
from leitura_arquivo_drive import *

# Caminho para a credencial da conta de serviço
CREDENTIALS_PATH = 'credentials/people-analytics-pipoca-agil-google-drive.json'

# Transformação de dados
class DataTransformer:
    def __init__(self, df_raw,file_name):
        self.df_raw = df_raw
        self.file_name = file_name
    
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
    
    def adicionar_caderno_pergunta(self):
        if file_name == 'autoavaliacao.xlsx':
            self.df_raw['nmCadernoPergunta'] = 'Autoavaliação Pipoca Ágil (respostas)'

    def clean_empty_rows(self):
        df_copy = self.df_raw
        df_copy = df_copy.drop_duplicates()
        self.df_raw = df_copy
            
    def transformar_dados(self):
        self.renomear_colunas_autoavaliacao()
        self.validar_email()
        self.df_raw['timestamp'] = self.df_raw['timestamp'].apply(self.padronizar_datastring)
        self.adicionar_caderno_pergunta()
        self.clean_empty_rows()
        return self.df_raw
#para transformar o arquivo autoavaliacao da pasta trusted no formato modelo_fato_respostas
class TransformerFatoRespostas:
    def __init__(self,df_trusted):
        self.df_trusted = df_trusted


    def transformar_trusted_fato_respostas(self):
        df_copy = self.df_trusted
        #criaremos colunas de informações que são comuns a todos os relatórios
        #coluna com a descrição do tipo de pergunta
        tipo_perguntas = ['Quantitativa de 0 a 10','Quantitativa de 0 a 10','Quantitativa de 0 a 10','Quantitativa de 0 a 10',
                  'Quantitativa de 0 a 10','Quantitativa de 0 a 10','Quantitativa de 0 a 10,','Quantitativa de 0 a 10',
                  'sim/nao','Quantitativa de 0 a 10','Quantitativa de 0 a 10','Quantitativa de 0 a 10',
                  'Quantitativa de 0 a 10','Quantitativa de 0 a 10','Quantitativa de 0 a 10','Quantitativa de 0 a 10',
                  'Descritiva, texto de opinião']
        #coluna com o tipo de dados das respostas
        tipo_repostas = ['int','int','int','int','int','int','int','int','boolean','int','int','int','int','int','int','int',
                 'str']
        #coluna com as perguntas
        perguntas = df_copy.keys().tolist()[5:22]
        #Cada entrevistado, que representa uma linha, que terá que ser transposta separadamente, transformado em dataframe e depois
#os dataframes serão concatenados verticalmente
        all_df = []
        for i_entrevistado in range(df_copy.shape[0]):
            row = df_copy.iloc[i_entrevistado].T
            row = row.apply(lambda x: int(x) if pd.notna(x) and isinstance(x, (np.float64, float)) else x) #transformar todos os campos float para integer
            fato_resposta = {'timestamp': "Placeholder",
                             'dsEmailRespondente': row.iloc[1], #campo do email
                              'dsNomeRespondente': row.iloc[2], #campo do entrevistado    
                              'dsQualFuncaoDesempenha':row.iloc[3], #campo da função
                              'dsEquipeParticipante':row.iloc[4], #campo da equipe
                              'nmCadernoPergunta': 'Autoavaliação Pipoca Ágil (respostas)', #modificar para cada formulário
                              'dsTituloPergunta': perguntas, #lista com as perguntas
                              'dsTipoPergunta':tipo_perguntas, #lista com o tipo das perguntas
                              'dsResposta':row.iloc[5:22], #lista com as respotas
                              'dsDataType':tipo_repostas} #lista com os tipos das respostas
            df_fato_resposta = pd.DataFrame(fato_resposta).reset_index(drop=True) #criar um dataframe do dicionário fato_reposta
        all_df.append(df_fato_resposta) #unir todos os dataframes en uma lista
        df_new = pd.concat(all_df)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_new['timestamp']=timestamp
        return df_new

# Processo principal de transformação do raw para o trusted
def processar_arquivo(drive_manager, file_name,relatorio_raw):
    drive_manager = GoogleDriveManager()
    folder_id = drive_manager.Id_camada['raw'] #obter o id da pasta raw
    file_id = drive_manager.get_file_id(relatorio_raw,folder_id) #obter o id do arquivo relatorio
    drive_manager.download_existing_file(file_id, file_name)
    df_raw = pd.read_excel(file_name)
    transformer = DataTransformer(df_raw,file_name)
    df_transformado = transformer.transformar_dados()
    for camada in ['trusted']:
        drive_manager.save_data_to_layer(df_transformado,camada,relatorio_raw)
    file_to_save = f"{relatorio_raw}"+"_processado.xlsx"
    df_transformado.to_excel(file_to_save)

#processo para transformar trusted em refined, no modelo da fato_respostas
def processar_fato_respostas(drive_manager, transformer,relatorio):
    data = transformer.transformar_trusted_fato_respostas()
    for camada in ['refined']:
        drive_manager.save_data_to_layer(data.copy(),camada,relatorio)

# Executar o processamento
if __name__ == "__main__":
    setup_logging()
    # IDs das pastas
    file_name = "autoavaliacao.xlsx"
    relatorio = "autoavaliacao"
    relatorio_final = 'modelo_fato_respostas.xlsx'
    #autenticação e o Google Drive Manager serão comuns a todos
    auth = GoogleAuthenticator()
    drive_manager = GoogleDriveManager(auth.drive_service)
    #transformação do arquivo raw no trusted
    processar_arquivo(drive_manager,file_name,relatorio)
    #transformação do arquivo trusted em fato_respotas
    df_trusted = pd.read_excel(f"{relatorio}"+"_processado.xlsx")
    transformer = TransformerFatoRespostas(df_trusted)
    processar_fato_respostas(drive_manager,transformer,relatorio_final)

 

