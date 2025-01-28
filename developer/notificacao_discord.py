# IMPORTANDO AS BIBLIOTECAS NECESSARIAS:
import requests
from datetime import datetime

# FUNÇÃO QUE ENVIA NOTIFICAÇÃO PARA O DISCORD

# URL do webhook do Discord, Canal Observabilidade
URL_WEBHOOK = "https://discord.com/api/webhooks/1333091809139621939/aMNr3JAmrpzklttIUStqdp8W2BNPU91GNRzHPaPe3NjBiqHs69vVqbyw34I_FY0Aaf01"

def enviar_notificacao_discord(mensagem, status="info"):
    """
    Envia uma notificação para o Discord usando um webhook.

    Args:
        mensagem (str): Texto da mensagem a ser exibida.
        status (str): Status da mensagem: "info", "sucesso", "erro".
    """
    # Cores baseadas no status
    cores = {
        "info": 3447003,     # Azul
        "sucesso": 3066993,  # Verde
        "erro": 15158332     # Vermelho
    }

    # Timestamp atual no formato ISO8601
    timestamp = datetime.now().isoformat()

    # Corpo da mensagem
    conteudo = {
        "username": "Bender",  # Nome do bot que aparece no Discord
        "embeds": [
            {
                "title": f"ETL - {status.capitalize()}",
                "description": mensagem,
                "color": cores.get(status, 3447003),  # Azul é a cor padrão
                "timestamp": timestamp,
            }
        ]
    }

    # Enviar requisição para o webhook
    resposta = requests.post(URL_WEBHOOK, json=conteudo)

    # Verificar sucesso
    if resposta.status_code == 204:
        print("Notificação enviada com sucesso!")
    else:
        print(f"Erro ao enviar notificação: {resposta.status_code} - {resposta.text}")

# Exemplos de chamadas da função
enviar_notificacao_discord("O processo ETL foi iniciado por Larissa.", status="info")

# Exemplos de chamadas da função
# enviar_notificacao_discord("O processo ETL foi iniciado.", status="info")
# enviar_notificacao_discord("A transformação de dados foi concluída.", status="sucesso")
# enviar_notificacao_discord("Erro ao carregar os dados no banco de dados.", status="erro")