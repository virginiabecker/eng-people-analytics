# Documentação Completa do Projeto People Analytics - Pipoca Ágil

## 1. Visão Geral do Projeto

O projeto tem como objetivo a extração, transformação e carga (ETL) de dados do Google Drive, processando informações de autoavaliação para um ambiente refinado, e enviando notificações para um canal no Discord.

## 2. Principais Ferramentas Utilizadas

O projeto utiliza diversas bibliotecas e serviços gratuitos, trazendo benefícios como escalabilidade, custo reduzido e facilidade de integração.

- **Pandas**: Manipulação e análise de dados estruturados.
- **Google Drive API**: Extração e armazenamento de arquivos no Google Drive.
- **Requests**: Envio de mensagens para o Discord via Webhook.
- **Datetime**: Trabalha com datas e timestamps.
- **Re (Regex)**: Processamento de strings e padronização de texto.
- **Dateutil**: Conversão e tratamento de datas flexíveis.
- **Python**: Versão 3.11

## 3. Arquitetura do Projeto

O projeto segue a metodologia ETL, dividida nas seguintes etapas:

1. **Extração de Dados**: Download de arquivos do Google Drive.
2. **Transformação de Dados**: Padronização, limpeza e estruturação dos dados.
3. **Carga dos Dados**: Upload dos arquivos transformados para a pasta final.
4. **Notificação**: Envio de mensagens para o Discord informando o status do processamento.

## 4. Detalhamento das Classes e Funções

### 4.1. **GoogleDriveManager**

Gerencia a autenticação e manipulação de arquivos no Google Drive.

#### Métodos:

- `authenticate()`: Realiza a autenticação usando credenciais de conta de serviço.
- `get_file_by_name(folder_id, file_name)`: Busca um arquivo específico no Google Drive.
- `download_excel(file_id)`: Faz o download de um arquivo Excel do Drive.
- `upload_file(folder_id, file_name, file_path)`: Faz o upload de um arquivo processado para o Drive.

### 4.2. **DataExtractor**

Responsável por carregar o arquivo Excel extraído do Google Drive.

#### Métodos:

- `load_excelfile()`: Realiza o carregamento do arquivo e converte em DataFrame do Pandas.

### 4.3. **DataTransformer**

Padroniza, renomeia e ajusta os dados da autoavaliação.

#### Métodos:

- `renomear_colunas_autoavaliacao()`: Ajusta nomes das colunas do DataFrame.
- `validar_email()`: Verifica se os e-mails estão no padrão correto.
- `padronizar_datastring(dataStamp)`: Converte strings para o formato de data padronizado.
- `adicionar_caderno_pergunta()`: Adiciona a informação do questionário ao DataFrame.
- `clean_empty_rows()`: Remove linhas duplicadas e vazias do DataFrame.

### 4.4. **TransformerFatoRespostas**

Transforma os dados da autoavaliação para um modelo de "fato respostas".

#### Métodos:

- `criar_fato_respostas()`: Cria a estrutura inicial do DataFrame "fato respostas".
- `add_info(df_fato_resposta)`: Preenche o DataFrame com os dados extraídos e transformados.
- `salvar_fato_resposta()`: Salva o arquivo processado na camada "refined" do Google Drive.

### 4.5. **DiscordNotifier**

Classe responsável por enviar notificações sobre o processo ETL para um canal do Discord.

#### Métodos:

- `enviar_notificacao(mensagem, processo, status)`: Envia uma mensagem para o Discord.

## 5. Benefícios do Uso de Ferramentas Gratuitas

- **Google Drive API**: Permite armazenar e compartilhar arquivos sem custo até um limite.
- **Pandas**: Biblioteca poderosa para análise de dados.
- **Requests**: Biblioteca fácil de usar para interação com APIs.
- **Discord Webhook**: Notificações em tempo real sem necessidade de servidores dedicados.

## 6. Possíveis Melhorias Futuras

1. **Automatização com Cloud Functions**: Executar o processo de ETL automaticamente com Google Cloud Functions.
2. **Dashboards Interativos**: Implementação de dashboards com Power BI ou Google Data Studio.
3. **Armazenamento em Banco de Dados**: Em vez de salvar no Google Drive, os dados podem ser armazenados em um banco como BigQuery ou PostgreSQL.
4. **Monitoramento Aprimorado**: Melhorar logs e alertas via Discord e e-mail.

## 7. Conclusão

O projeto People Analytics - Pipoca Ágil é uma solução eficiente para coletar, transformar e analisar dados de autoavaliação. O uso de ferramentas gratuitas reduz custos e permite um sistema escalável e flexível. As melhorias futuras visam aumentar a automação e fornecer insights mais aprofundados.

---

Caso tenha dúvidas ou precise de melhorias, entre em contato com a equipe de desenvolvimento! 🚀

