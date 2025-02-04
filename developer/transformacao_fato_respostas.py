from leitura_arquivo_drive import *
from transformacao_autoavaliacao import GoogleDriveManager,DataExtractor
import pandas as pd

class TransformerFatoRespostas:

    def __init__(self, df_padronizado):
        self.df_padronizado =df_padronizado
        #self.df_fato_resposta = self.criar_fato_respostas()

    def criar_fato_respostas(self):
        fato_resposta = {'timestamp': [],
                             'dsEmailRespondente': [],
                              'dsNomeRespondente': [],
                              'dsQualFuncaoDesempenha':[],
                              'dsEquipeParticipante':[],
                              'nmCadernoPergunta':[],
                              'dsTituloPergunta':[],
                              'dsTipoPergunta':[],
                              'dsResposta':[],
                              'dsDataType':[]}
        df_fato_resposta = pd.DataFrame(fato_resposta)
        return df_fato_resposta
    
    #Função para adicionar as informações do
    def add_info(self,df_fato_resposta):
        df_fato_resposta['timestamp'] = self.df_padronizado['timestamp']
        df_fato_resposta['dsEmailRespondente'] = self.df_padronizado['emailRespondente']
        df_fato_resposta['dsNomeRespondente']                     
        df_fato_resposta['dsQualFuncaoDesempenha']                      
        df_fato_resposta['dsEquipeParticipante']                      
        df_fato_resposta['nmCadernoPergunta']                     
        df_fato_resposta['dsTituloPergunta']                      
        df_fato_resposta['dsTipoPergunta']                      
        df_fato_resposta['dsResposta']                     
        df_fato_resposta['dsDataType']                     
        
             
    def criar_fato_resposta(self)
        

    
    def salvar_fato_resposta(self):
        data = self.df_fato_resposta.values.tolist()
        camada = 'refined'
        relatorio = 'fato_respostas'
        GoogleDriveManager.save_data_to_layer(data, camada, relatorio)

folder_id_destino = '1tc3HQnG507HfyLvHqtZasb-La8GD98P0' #pasta people_analytics/refined/
folder_id_origem = "1WJlq1C_uLq9J3Ta-lVAkQVv7AzblftsD" #pasta people_analytics/trusted/ 
file_name = "autoavalicao_pipoca.xlsx_processado.xlsx"