# Documentação Fato Respostas

## Visão Geral
Este projeto tem como objetivo processar e transformar dados de respostas de avaliação armazenados no Google Drive. Ele lê arquivos de entrada, realiza transformações nos dados e salva os resultados na camada "refined" do Google Drive.

## Dependências
O projeto depende dos seguintes módulos:

- **leitura_arquivo_drive**: Módulo responsável pela leitura de arquivos no Google Drive.
- **transformacao_autoavaliacao**: Contém classes para autenticação e manipulação de dados.
- **pandas**: Utilizado para manipulação e transformação de dados tabulares.

## Classes e Funções

### `TransformerFatoRespostas`
Classe principal para processar e estruturar os dados de respostas de avaliação.

#### Métodos

- `__init__(self, df_padronizado)`: Inicializa a classe com um DataFrame contendo os dados padronizados.
- `criar_fato_respostas(self)`: Cria um DataFrame vazio com colunas padronizadas para armazenar respostas processadas.
- `add_info(self, df_fato_resposta)`: Adiciona informações do DataFrame padronizado ao DataFrame de fato respostas.
- `salvar_fato_resposta(self)`: Salva os dados processados no Google Drive na camada "refined".

## Fluxo de Processamento
1. **Leitura do arquivo de entrada**: O arquivo `autoavalicao_pipoca.xlsx_processado.xlsx` é lido do Google Drive na pasta "trusted".
2. **Criação do DataFrame de fato respostas**: Um novo DataFrame é criado para armazenar os dados estruturados.
3. **Transformação dos dados**: Os dados são organizados em colunas padronizadas.
4. **Salvamento no Google Drive**: Os dados transformados são enviados para a pasta "refined" no Google Drive.

## Configuração de Diretórios

- **Pasta de Origem (trusted)**: `1WJlq1C_uLq9J3Ta-lVAkQVv7AzblftsD`
- **Pasta de Destino (refined)**: `1tc3HQnG507HfyLvHqtZasb-La8GD98P0`
- **Nome do Arquivo de Entrada**: `autoavalicao_pipoca.xlsx_processado.xlsx`

## Melhorias Futuras
- Correção de erros na função `add_info`, pois algumas colunas não estão sendo preenchidas corretamente.
- Implementar `criar_fato_resposta(self)`, pois a função está incompleta.
- Testes automatizados para validar a transformação de dados.

## Conclusão
Este projeto visa padronizar e armazenar respostas de autoavaliação, garantindo integridade e disponibilidade dos dados para futuras análises.

