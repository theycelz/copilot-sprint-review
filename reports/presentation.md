---
marp: true
theme: default
class: lead
paginate: true
backgroundColor: #ffffff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# Avaliação do Experimento: Review Automatizado com GitHub Copilot
## Análise Comparativa Sprint 1-2 vs Sprint 3-4

**Projeto FarmVet**
28/11/2025

---

## Contexto & Metodologia

**O que foi testado?**
Implementação de revisão de Pull Requests assistida por Agente GitHub Copilot.

**Período de Análise**
- **Baseline (Sprint 1-2)**: 02/09 a 20/10 (Revisão Humana Tradicional)
- **Experimental (Sprint 3-4)**: 21/10 a 28/11 (Revisão Híbrida com Copilot)

**Hipótese**
> "Revisões automatizadas reduziriam o tempo de ciclo (Time to Merge) mantendo a qualidade do código."

---

## Resultado Principal

![width:900px](docs/analysis_plots/01_impacto_tempo_merge.png)

### O tempo mediano até o merge caiu 95% (de 15.1h para 0.75h).

---

## Métricas Quantitativas

![width:900px](docs/analysis_plots/02_metricas_resumidas.png)

*Diferença estatisticamente significativa (Mann-Whitney U, p < 0.01)*

---

## Análise de Trade-offs

| ✅ Ganhos Claros | ⚠️ Pontos de Atenção |
| :--- | :--- |
| **Velocidade**: Ciclos de feedback quase instantâneos (45 min). | **Aumento de Bugs/Fixes**: Taxa de PRs do tipo "fix" subiu de 3.9% para 15.2%. |
| **Padronização**: Aderência a Conventional Commits subiu de 53% para 77%. | **Menor Interação Humana**: Queda de 59% nos comentários por PR. |
| **Desbloqueio**: Menos PRs parados esperando "olhadinha". | **Risco de Complacência**: Desenvolvedores podem confiar cegamente no bot. |

---

## Correlação com Feedback Qualitativo

> "100% dos participantes relataram economia de tempo e recomendam a adoção."

**Resultados do Survey (N=6):**
*   **Experiência**: 4/6 "Melhor", 2/6 "Muito Melhor".
*   **Economia Percebida**: 4/6 sentiram economia > 50% (Corrobora o dado quantitativo de 86%).
*   **Pontos de Atenção**: Copilot deixou passar **Bugs Lógicos** e **Segurança** em alguns casos.

**Conclusão**: A percepção do time está alinhada com os dados. A velocidade é sentida, mas a segurança exige revisão humana.

---

## Análise Crítica e Riscos
*   **Ameaça à Qualidade**: A taxa de retrabalho quadruplicou (3.9% -> 15.2%). O código sai rápido, mas volta rápido para correção.
*   **Complacência**: A queda de 59% nos comentários sugere revisões mais superficiais ("LGTM Syndrome").
*   **Viés de Contexto**: Parte da velocidade deve-se à fase final do projeto (Sprint 4), não apenas à IA.
*   **Limitação da IA**: Falha em lógica de negócio complexa e segurança.

---

## Veredito
### ✅ ADOTAR O GITHUB COPILOT

**Justificativa**: O ganho de agilidade (95% menos tempo de merge) é transformador. Os riscos de qualidade (aumento de fixes) são gerenciáveis com CI/CD robusto e revisão humana atenta.

**Próximos Passos**:
1.  **Refinar Prompt**: Ajustar o Agente para ser menos verboso em questões triviais.
2.  **Monitorar Produção**: Verificar se o aumento de "fix" em PRs vira bugs para o usuário.vação humana para garantir contexto de negócio.
3.  **Monitorar Qualidade**: Acompanhar se a taxa de bugs em produção aumenta (não apenas PRs de fix).

---

# Obrigado!

**Dúvidas?**
Acesse o Dashboard Interativo em `docs/metrics_dashboard.html`
