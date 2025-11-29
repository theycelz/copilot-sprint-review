# Coleta de Métricas de PRs - FarmVet

Este script coleta métricas de Pull Requests dos repositórios `PDS-Farmvet/backend` e `PDS-Farmvet/frontend` para comparar a performance entre as Sprints 1-2 (Baseline) e Sprints 3-4 (Experimental).

## Pré-requisitos

- Python 3
- GitHub CLI (`gh`) autenticado

## Instalação

1. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Execute o script:
```bash
python collect_metrics.py
```

O script irá gerar um relatório no terminal e salvar os dados detalhados em `pr_metrics_analysis.csv`.

## Configuração

As datas das sprints e os repositórios estão definidos no início do arquivo `collect_metrics.py` e podem ser ajustados conforme necessário.
