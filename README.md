# Projeto People Analytics Pipoca Ágil

Este repositório contém um projeto de Engenharia de Dados que utiliza **ferramentas open source**, **Python** e **GitHub** para criar uma solução escalável e eficiente para o processamento e análise de dados do projeto voluntário Pipoca Ágil.

---

## 📖 Visão Geral

O objetivo deste projeto é construir um pipeline de dados low cost e que entregue valor ao negócio. O projeto aproveita o **Python** como linguagem de programação principal, **GitHub** como plataforma para versionamento e integração contínua, **Windowns Scheduler** como ferramenta de orquestração e **Discord** como ferramenta para observabilidade da execução dos pipelines.

---

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem de programação principal para desenvolvimento da pipeline de dados.
- **GitHub**: Gerenciamento de código-fonte, controle de versão e integração contínua.
- **Windowns Scheduler***: Para orquestração dos pipelines
- **Discord**: Como ferramenta de observabilidade

---

## 🚀 Estrutura do Projeto

```plaintext
.
├── app/                                            # Código-fonte principal
│   ├── avaliacao_projeto.py                        # Arquivo python de ETL do formulário de avaliacao do projeto
│   ├── avaliacao_coletiva.py                       # Arquivo python de ETL do formulário de avaliacao coletiva
│   ├── avaliacao_individual.py                     # Arquivo python de ETL do formulário de avaliacao individual
│   ├── autoavalicao.py                             # Arquivo python de ETL do formulário de autoavalicao
│   ├── requirements.txt                            # Dependências do projeto
│   └── utils/                                      # Scripts utilitários
├── developer/                                      # Código-fonte desenvolvimento
│   ├── script.ipynb                                # Arquivo Jupyter Notebook para desenvolvimento
├── README.md                                       # Documentação do projeto
├── png/                                            # Imagens do projeto
│   ├── arquitetura_dados_people_analytics.png      # Arquivo png com imagem da arquitetura de dados

```
---

## 🚀 Arquitetura de dados People Analytics

![Arquitetura de dados People Analytics](/png/arquitetura_dados_people_analytics.png)