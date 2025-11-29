# Avaliação do Experimento GitHub Copilot - FarmVet

Este diretório contém todos os scripts, dados e relatórios da análise comparativa do uso do GitHub Copilot no processo de revisão de código do projeto FarmVet.

## Estrutura

- **scripts/**: Códigos Python utilizados para coleta, análise e visualização.
  - `collect_metrics.py`: Extrai dados do GitHub.
  - `analyze_metrics.py`: Realiza testes estatísticos.
  - `visualize_metrics.py`: Gera gráficos e dashboard.
  - `analyze_qualitative.py`: Processa dados do survey.
- **data/**: Dados brutos e processados (CSV).
- **reports/**: Documentação e apresentações.
  - `presentation.md`: Slides da apresentação executiva.
  - `technical_report.md`: Relatório técnico detalhado.
  - `executive_summary.txt`: Resumo em 1 parágrafo.
- **results/**: Artefatos visuais gerados.
  - `analysis_plots/`: Imagens PNG dos gráficos.
  - `metrics_dashboard.html`: Dashboard interativo.

## Como Reproduzir

1. Instale as dependências:
   ```bash
   pip install -r scripts/requirements.txt
   ```

2. Execute os scripts na ordem:
   ```bash
   python scripts/collect_metrics.py
   python scripts/analyze_metrics.py
   python scripts/visualize_metrics.py
   ```
