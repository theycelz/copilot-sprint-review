# Relatório Técnico: Avaliação do Experimento com GitHub Copilot

**Data:** 28/11/2025
**Projeto:** FarmVet (Backend & Frontend)

---

## 1. Resumo Executivo

Este relatório detalha a metodologia e os resultados da análise comparativa entre o processo de revisão de código tradicional (Sprints 1-2) e o processo experimental assistido pelo GitHub Copilot (Sprints 3-4).

**Conclusão Principal:** A introdução do Copilot reduziu drasticamente o tempo de ciclo (Time to Merge) em **~86%** (mediana), com aumento significativo na aderência aos padrões de commit (+22%).

---

## 2. Metodologia

### 2.1 Coleta de Dados

A extração de dados foi realizada de forma automatizada utilizando a API do GitHub via CLI (`gh`).

*   **Ferramentas**: Python 3.12, Pandas, GitHub CLI.
*   **Script de Coleta**: `scripts/collect_metrics.py`
*   **Fontes de Dados**:
    *   Repositório Backend: `PDS-Farmvet/backend`
    *   Repositório Frontend: `PDS-Farmvet/frontend`
*   **Períodos Analisados**:
    *   **Baseline (Sprint 1-2)**: 02/09/2025 a 20/10/2025.
    *   **Experimental (Sprint 3-4)**: 21/10/2025 a 28/11/2025.

**Métricas Extraídas:**
*   `createdAt`, `mergedAt`: Para cálculo do *Time to Merge*.
*   `comments`, `reviews`: Para volume de interação.
*   `additions`, `deletions`: Para categorização por tamanho (*Size*).
*   `title`: Para análise de aderência semântica (*Conventional Commits*).

### 2.2 Análise Estatística

Os dados brutos foram processados para remover ruídos e calcular métricas derivadas.

*   **Script de Análise**: `scripts/analyze_metrics.py`
*   **Testes de Hipótese**:
    *   **Shapiro-Wilk**: Para verificar normalidade das distribuições (Resultou em não-normal para ambas as fases).
    *   **Mann-Whitney U**: Teste não-paramétrico escolhido para comparar as medianas de tempo, dado a não-normalidade.
*   **Métricas de Qualidade (Proxies)**:
    *   **Fix Rate**: Porcentagem de PRs iniciados com "fix" (indicativo de correção de bugs ou ajustes rápidos).
    *   **Semantic Adherence**: Validação via Regex do padrão de títulos.

### 2.3 Visualização

*   **Script de Visualização**: `scripts/visualize_metrics.py`
*   **Ferramentas**: Matplotlib, Seaborn, Plotly.
*   Geração de gráficos estáticos para apresentação e dashboard interativo HTML.

---

## 3. Resultados Detalhados

### 3.1 Velocidade (Time to Merge)

Houve uma redução estatisticamente significativa no tempo de merge.

| Métrica | Baseline (Sprint 1-2) | Experimental (Sprint 3-4) | Variação |
| :--- | :--- | :--- | :--- |
| **Média** | 55.68 h | 15.58 h | -72.0% |
| **Mediana** | **15.14 h** | **0.75 h** | **-95.0%** |
| **Desvio Padrão** | 84.91 h | 34.20 h | -59.7% |

*   **Teste Estatístico**: Mann-Whitney U (p-value = 0.0011 < 0.05). **Resultado Significativo.**

### 3.2 Interação e Qualidade

| Métrica | Baseline | Experimental | Variação |
| :--- | :--- | :--- | :--- |
| **Comentários/PR (Média)** | 0.71 | 0.29 | -59% |
| **Reviews/PR (Média)** | 1.24 | 2.58 | +108% |
| **Aderência Semântica** | 52.9% | 77.2% | +24.3 p.p. |
| **Taxa de Fix (Bugs)** | 3.9% | 15.2% | +11.3 p.p. |

### 3.3 Análise de Distribuição

A distribuição do tempo de merge na fase experimental tornou-se muito mais concentrada em valores baixos (curva leptocúrtica à esquerda), indicando um fluxo de "Fast Track" para a maioria dos PRs.

### 3.3 Análise de Comportamento e Contexto do Projeto

Uma análise detalhada dos PRs mais rápidos da fase experimental (mediana de 0.75h) revela uma mudança significativa no fluxo de trabalho, que deve ser interpretada considerando dois fatores:

1.  **Efeito "Reta Final" (Sprint 4)**: A fase experimental coincidiu com a entrega final do produto. É natural que, neste estágio, ocorra um volume maior de pequenos ajustes (`hotfix`, `style`, `chore`) para polimento, o que contribui para a redução do tempo médio de merge independente da ferramenta.
2.  **Facilitação pelo Copilot**: Embora o momento do projeto exija rapidez, o Copilot atuou como um *facilitador* crítico, permitindo que esses ajustes fossem gerados e corrigidos com fricção mínima. A ferramenta suportou bem o ritmo frenético de "Micro-PRs" exigido pelo final do projeto.

Portanto, a redução de 95% é um resultado composto: **Contexto de Final de Projeto + Agilidade proporcionada pela IA**.

### 3.4 Análise Qualitativa (Survey)

Os dados quantitativos foram corroborados pela pesquisa com os desenvolvedores:

*   **Satisfação**: 100% dos participantes relataram uma experiência "Muito Boa" ou "Boa".
*   **Economia de Tempo**: A percepção subjetiva foi de uma economia de 40-50% no tempo de desenvolvimento.
*   **Blind Spots**: Os devs notaram que o Copilot pode deixar passar bugs de lógica complexa, o que alinha com o aumento na taxa de `fix` observada nos dados (15.2%).

## 4. Conclusão e Recomendações

O experimento foi um sucesso. A ferramenta provou ser um acelerador essencial, especialmente no contexto de entrega final.

### Recomendações:
1.  **Adotar Definitivamente**: O ganho de velocidade é inegável, especialmente para tarefas repetitivas e ajustes finais.
2.  **Monitorar Qualidade**: O aumento de bugs/fixes (de 3.9% para 15.2%) exige atenção. Recomenda-se reforçar testes automatizados (CI) para mitigar o retrabalho.
3.  **Reforçar Code Review**: Para PRs complexos, a revisão humana continua indispensável. A queda de 59% nos comentários alerta para a necessidade de manter o rigor.
4.  **Considerar o Viés**: Em futuras medições, comparar períodos de desenvolvimento de features (início de sprint) para isolar melhor o impacto da IA.

---

## Apêndice: Ferramentas Utilizadas

Todo o código fonte para esta análise encontra-se no diretório `scripts/` do repositório:
- `collect_metrics.py`: Extração.
- `analyze_metrics.py`: Estatística.
- `visualize_metrics.py`: Gráficos.
