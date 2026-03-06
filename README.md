# Avaliação do GitHub Copilot em Code Review

Análise experimental do impacto do GitHub Copilot na revisão de Pull Requests do projeto FarmVet, comparando sprints com revisão humana tradicional (baseline) vs revisão híbrida com IA (experimental).

## Resultados Principais

| Métrica | Baseline (Sprint 1-2) | Experimental (Sprint 3-4) | Variação |
|---------|----------------------|--------------------------|----------|
| **Tempo mediano de merge** | 15.1h | 0.75h | **-95%** |
| **Comentários/PR** | 0.71 | 0.29 | -59% |
| **Reviews/PR** | 1.25 | 2.58 | +108% |
| **Aderência semântica** | 52.9% | 77.2% | +24 p.p. |
| **Taxa de fix** | 3.9% | 15.2% | +11 p.p. |

Diferença estatisticamente significativa (Mann-Whitney U, p < 0.01, Cohen's d = 0.67).

## Metodologia

- **Coleta**: Extração automatizada via GitHub CLI de ~143 PRs merged entre Set-Nov/2025
- **Análise**: Shapiro-Wilk (normalidade), Mann-Whitney U (comparação), Cohen's d (tamanho do efeito)
- **Qualitativa**: Survey com 6 desenvolvedores (100% recomendaram adoção)

## Estrutura

```
scripts/
  collect_metrics.py      # Extração de dados via gh CLI
  analyze_metrics.py      # Testes estatísticos (Shapiro-Wilk, Mann-Whitney, Cohen's d)
  analyze_qualitative.py  # Análise do survey
  visualize_metrics.py    # Gráficos (matplotlib/seaborn) e dashboard (plotly)
data/                     # CSVs com métricas brutas e processadas
reports/
  technical_report.md     # Relatório técnico completo
  presentation.md         # Slides (Marp)
  executive_summary.txt   # Resumo executivo
results/
  analysis_plots/         # Gráficos gerados
  metrics_dashboard.html  # Dashboard interativo
```

## Como Reproduzir

```bash
pip install -r scripts/requirements.txt
python scripts/collect_metrics.py       # requer gh CLI autenticado
python scripts/analyze_metrics.py
python scripts/analyze_qualitative.py
python scripts/visualize_metrics.py
```

## Conclusão

O Copilot reduziu drasticamente o ciclo de revisão, mas a taxa de retrabalho quadruplicou (3.9% → 15.2%). Recomendação: **adotar com revisão humana obrigatória para PRs complexos** e monitoramento de bugs em produção.

## Licença

MIT
