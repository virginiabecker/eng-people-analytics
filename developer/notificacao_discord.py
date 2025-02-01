import requests
from datetime import datetime

class DiscordNotifier:
    """
    Classe para enviar notificações ao Discord via webhook.
    """    
    def __init__(self):
        """
        Inicializa a classe com a URL do webhook do Discord.

        Args:
            webhook_url (str): URL do webhook do Discord.
        """
        self.webhook_url = "https://discord.com/api/webhooks/1333091809139621939/aMNr3JAmrpzklttIUStqdp8W2BNPU91GNRzHPaPe3NjBiqHs69vVqbyw34I_FY0Aaf01"

    def enviar_notificacao(self, mensagem, processo, status="info"):
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
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Corpo da mensagem
        conteudo = {
            "username": "Bender",  # Nome do bot que aparece no Discord
            "embeds": [
                {
                    "title": f"Processo: {processo.capitalize()}",
                    "description": mensagem,
                    "color": cores.get(status, 3447003),  # Azul é a cor padrão
                    "timestamp": timestamp,
                }
            ]
        }

        # Enviar requisição para o webhook
        resposta = requests.post(self.webhook_url, json=conteudo)

        # Verificar sucesso
        if resposta.status_code == 204:
            print("Notificação enviada com sucesso!")
        else:
            print(f"Erro ao enviar notificação: {resposta.status_code} - {resposta.text}")

# Exemplo de uso
if __name__ == "__main__":

    notifier = DiscordNotifier()
    notifier.enviar_notificacao("O processo de ETL foi iniciado.", processo='XPTO', status="info")