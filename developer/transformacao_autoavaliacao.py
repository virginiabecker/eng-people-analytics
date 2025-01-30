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
       email e nome dos participantes. 
       Arg: dataframe com as respostas do questionário.'''
    def __init__(self,df_raw):
        self.df_raw=df_raw
    '''Função para padronizar uma pergunta, removendo caracteres especiais, pontuação e acentos.'''
    def retirar_acento(frase):
        nova = frase.lower()
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

    '''Função para validar os emails preenchidos usando regex. Essa funçao deve ser aplicada a cada string'''
    def verificar_email(email):
        padraoEmail = r'^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$'
        padraoCorreto = re.compile(padraoEmail)
        if not re.match(padraoCorreto,email):
           return "Email Incorreto"
        else:
           return "Pass"
        
    '''Função para padronizar as datas do datestamp'''
    def padronizar_datastring(dataStamp):
        dt = parse(str(dataStamp))
        return dt.strftime("%d-%m-%Y %H:%M:%S") 
    
    '''Função para validar os nomes. Eles devem ter pelo menos 3 letras, não podem começar com números e o campo deve ser uma string.'''
    def verificar_nome(nome,minlen=3):
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
        self.df_raw = df_renomeada
        
    '''Função final para validar o email preenchido no formulário'''
    def validar_email(self):
        df_copy = self.df_raw.copy()
        df_copy['emailRespondente'] = df_copy['emailRespondente'].apply(lambda x: x if self.verificar_email(x)=='Pass' else None)
        self.df_raw=df_copy

    '''Função para validar os nomes preenchidos no formulário'''
    def validar_nome(self):
        df_copy = self.df_raw.copy() 
        df_copy['nomeRespondente'] = df_copy['nomeRespondente'].apply(lambda x: x if self.verificar_nome is True else None)
        self.df_raw=df_copy

    '''Função final para padronizar as datas em d-m-Y H:M:S'''
    def padronizar_datas(self):
        df_copy = self.df_raw.copy()
        df_copy['timestamp'] = df_copy['timestamp'].apply(self.padronizar_datastring)
        self.df_raw=df_copy

    '''Função para aplicar a normalização de perguntas da primeira linha da tabela'''
    def normalizar_perguntas_df(self):
        df_copy = self.df_raw.copy()
        df_copy.iloc[0,2:]=df_copy.iloc[0,2:].apply(self.normalizar_perguntas)
        self.df_raw=df_copy


    '''Função com todas as etapas'''
    def transformar_dados(self):
        self.normalizar_perguntas_df()
        self.renomear_colunas_autoavaliacao()
        self.validar_email()
        self.validar_nome()
        self.padronizar_datastring()
        
        
