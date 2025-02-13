# Visão Geral  
Este projeto tem como objetivo extrair, transformar e carregar (ETL) dados armazenados em planilhas do Google Drive. Utiliza-se a API do Google Drive para acessar os arquivos e a biblioteca Pandas para a manipulação dos dados.  

---

## 1. Autenticação no Google Drive  
A classe `GoogleDriveManager` gerencia a autenticação na API do Google Drive e fornece métodos para interagir com arquivos.  

### 1.1 Autenticação  
A autenticação é realizada via uma conta de serviço utilizando credenciais armazenadas no arquivo JSON localizado em:  

```python
CREDENTIALS_PATH = 'credentials/people-analytics-pipoca-agil-google-drive.json'
1.2 Métodos Principais
get_file_by_name(folder_id_origem, file_name): Busca um arquivo pelo nome dentro de uma pasta no Google Drive.
download_excel(file_id): Faz o download de um arquivo Excel para um fluxo de bytes.
upload_file(folder_id_origem, file_name, file_path): Faz o upload de um arquivo para o Google Drive.
2. Extração de Dados
A classe DataExtractor é responsável por baixar os arquivos Excel do Google Drive.

2.1 Método Principal
load_excelfile(): Busca o arquivo no Google Drive e carrega os dados em um DataFrame Pandas.
3. Transformação de Dados
A classe DataTransformer é responsável por limpar e padronizar os dados.

3.1 Principais Funcionalidades
Normalização de Texto
retirar_acento(frase): Remove acentos de uma string.
normalizar_perguntas(pergunta): Converte perguntas para um formato padronizado.
Validação e Padronização
verificar_email(email): Valida e-mails.
padronizar_datastring(dataStamp): Converte datas para o formato dd-mm-yyyy HH:MM:SS.
renomear_colunas_autoavaliacao(): Renomeia colunas da planilha "autoavaliação".
validar_email(): Remove e-mails inválidos.
adicionar_caderno_pergunta(): Adiciona uma coluna identificando o tipo de questionário.
clean_empty_rows(): Remove linhas duplicadas.
Transformação Principal
transformar_dados(): Aplica todas as transformações ao DataFrame.
4. Processo Principal (ETL)
A função processar_arquivo executa todas as etapas do processo ETL.

4.1 Fluxo de Processamento
Extração: Baixa o arquivo do Google Drive.
Transformação: Aplica limpeza, normalização e validação de dados.
Carga: Salva o arquivo transformado no Google Drive.
4.2 Código Principal
python
Copiar
Editar
folder_id_origem = "1E6AEUGqRp3IJsWV4qAwMRJK_tMD7wDYT" # Pasta de origem (RAW)
folder_id_destino = "1WJlq1C_uLq9J3Ta-lVAkQVv7AzblftsD" # Pasta de destino (TRUSTED)
file_name = "autoavaliacao.xlsx"

processar_arquivo(folder_id_origem, folder_id_destino, file_name)
5. Estrutura de Pastas no Google Drive
people_analytics/raw/: Contém os arquivos brutos extraídos de questionários.
people_analytics/trusted/: Contém os arquivos transformados e validados.
6. Considerações Finais
Este projeto automatiza o processamento de dados de autoavaliação, garantindo qualidade e padronização das informações armazenadas. Caso novos questionários sejam adicionados, o código pode ser facilmente ajustado para suportá-los.


