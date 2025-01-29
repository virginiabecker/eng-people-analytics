import pandas as pd
import re
from  dateutil.parser import parse

#ler arquivo localmente e deixar a primeira linha como campo ao invés do nome da coluna
#planilha_autoavaliacao = pd.read_excel(r'autoavaliacao_pipoca_agil.xlsx',header=None)

class DataExtractor:
    """Classe para ler o arquivo"""
    def __init__(self,pathfile):
        self.pathfile = pathfile        
        
    def load_excelfile(self.pathfile):
        respostas_formulario = pd.read_excel(self.pathfile,header=None)


class DataTransformer:
    '''Essa classe vai reunir os métodos para padronização dos títulos das colunas, validação dos campos de data,
       email e nome dos participantes.'''
    def __init__(self,df_raw):
        self.df_raw=df_raw
    '''Função para padronizar as perguntas, removendo caracteres especiais, pontuação e acentos.'''
    def retirar_acento(palavras):
        nova = palavras.lower()
        nova = re.sub(r'[àáâãäå]', 'a', nova)
        nova = re.sub(r'[èéêë]', 'e', nova)
        nova = re.sub(r'[ìíîï]', 'i', nova)
        nova = re.sub(r'[òóôõö]', 'o', nova)
        nova = re.sub(r'[ùúûü]', 'u', nova)
        nova = re.sub(r'ç','c',nova)
        return nova
    
    def normalizar_perguntas(pergunta,retirar_acento):
        fase1 = pergunta.split('.')[1].lstrip()
        fase2 = re.sub(r'[^\w\s]','',fase1)
        fase3 = retirar_acento(fase2)
        fase4 = re.sub(' ','_',fase3)
        return fase4

    '''Função para validar os emails preenchidos'''
    
    def validar_email(email):
        padraoEmail = r'^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$'
        padraoCorreto = re.compile(padraoEmail)
        if not re.match(padraoCorreto,email):
           return "Email Incorreto"
        else:
           return "Pass"
        
    '''Função para padronizar as datas do datestamp'''
    def padronizar_data(dataStamp):
        dt = parse(str(dataStamp))
        return dt.strftime("%d-%m-%Y %H:%M:%S") 
    
    '''Função para validar os nomes. Eles devem ter pelo menos 3 letras, não podem começar com números e o campo deve ser uma string.'''
    def validar_nome(nome,minlen=3):
        if type(nome) !=str:
            return False
        elif len(nome)<minlen:
            return False
        elif not re.match('^[a-z0-9.-]*$',nome):
            return False
        elif nome[0].isnumeric():
            return False
        else:
            return True 
    '''Função para renomear os nomes das colunas e deixar elas mais legiveis.'''
    def renomear_colunas_autoavaliacao(self):
        df_renomeada = self.df_raw.copy()
        df_renomeada.columns = ['timestamp','emailRespondente','nomeRespondente','funcaoDesempenha','equipeParticipante',
                                  'dsCapacidadeConcluirSprint','dsSuporteInicioAtividades','ClarezaProgressoTimeSprint',
                                  'ParticipacaoDailiesReunioesImportantesSprint','dsCapacidadeConcluirTarefasPlanejadasSprint',
                                  'dsPresencaParticipacaoReunioesSprint','dsDisponibilidadeCumprirCompromissosSprint',
                                  'dsConfiancaCompreensaoPraticasScrum', 'dsTimeTemPapeisNecessariosScrumMasterPODesenvolvedoresUX/UIQA',
                                  'dsCapacidadeTimeConcluirTarefasPlanejadasSprint','dsRelevanciaProjeto','dsAlinhamentoProjetoObjetivoProfissional',
                                  'dsContribuicaoEntregaValor','dsNivelCompetenciaDesempenhoProjeto','dsContribuicaoQualidadeEntregas',
                                  'dsRegularidadeQualidadeComunicacaoTimeSprint','dsQueMelhorarAtuacao','dsComentarioSugestao']
        return df_renomeada
        
    
    '''Função com todas as etapas'''
    def transformar_planilhas(self,normalizar_perguntas,validar_email,padronizar_data,validar_nome,renomear_colunas_autoavaliacao):
        df_renomeada = renomear_colunas_autoavaliacao()
        df_renomeada.iloc[0,2:]=df_renomeada.iloc[0,2:].apply(normalizar_perguntas)
        df_renomeada['emailRespondente'] = df_renomeada['emailRespondente'].apply(validar_email)
        df_renomeada['nomeRespondente'] = df_renomeada['nomeRespondente'].apply(validar_nome)
        df_renomeada['timestamp'] = df_renomeada['timestamp'].apply(padronizar_data)
