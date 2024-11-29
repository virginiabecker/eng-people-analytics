# Projeto de Engenharia de Dados

Este repositório contém um projeto de Engenharia de Dados que utiliza **Google Cloud Run**, **Python** e **GitHub** para criar uma solução escalável e eficiente para o processamento e análise de dados.

---

## 📖 Visão Geral

O objetivo deste projeto é construir uma pipeline de dados moderna e serverless. O projeto aproveita o **Cloud Run** para executar jobs de processamento, **Python** como linguagem de programação principal e **GitHub** como plataforma para versionamento e integração contínua.

---

## 🛠️ Tecnologias Utilizadas

- **Google Cloud Run**: Serviço gerenciado para execução de contêineres serverless.
- **Python**: Linguagem de programação principal para desenvolvimento da pipeline de dados.
- **GitHub**: Gerenciamento de código-fonte, controle de versão e integração contínua.
- **Google Cloud Storage**: Para armazenar dados brutos e processados (opcional).
- **BigQuery**: Para análise de dados estruturados (opcional).

---

## 🚀 Estrutura do Projeto

```plaintext
.
├── app/                     # Código-fonte principal
│   ├── main.py              # Arquivo principal da aplicação
│   ├── requirements.txt     # Dependências do projeto
│   └── utils/               # Scripts utilitários
├── Dockerfile               # Configuração do contêiner
├── .github/
│   └── workflows/           # Configurações de CI/CD
│       └── deploy.yaml      # Pipeline de CI/CD
├── README.md                # Documentação do projeto
└── config/                  # Configurações do ambiente
    └── settings.yaml        # Configuração do projeto
