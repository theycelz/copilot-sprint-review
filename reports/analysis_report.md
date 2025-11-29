# Relatório de Análise Estatística de Métricas de PRs

## 1. Estatísticas Descritivas
| Phase                     |   ('Time to Merge (Hours)', 'mean') |   ('Time to Merge (Hours)', 'median') |   ('Time to Merge (Hours)', 'std') |   ('Time to Merge (Hours)', 'min') |   ('Time to Merge (Hours)', 'max') |   ('Comments', 'mean') |   ('Comments', 'median') |   ('Comments', 'std') |   ('Comments', 'min') |   ('Comments', 'max') |   ('Reviews', 'mean') |   ('Reviews', 'median') |   ('Reviews', 'std') |   ('Reviews', 'min') |   ('Reviews', 'max') |   ('Total Changes', 'mean') |   ('Total Changes', 'median') |   ('Total Changes', 'std') |   ('Total Changes', 'min') |   ('Total Changes', 'max') |
|:--------------------------|------------------------------------:|--------------------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|-----------------------:|-------------------------:|----------------------:|----------------------:|----------------------:|----------------------:|------------------------:|---------------------:|---------------------:|---------------------:|----------------------------:|------------------------------:|---------------------------:|---------------------------:|---------------------------:|
| Baseline (Sprint 1-2)     |                             53.5324 |                             13.9228   |                            83.8897 |                         0.00722222 |                            285.155 |               0.705882 |                        1 |              0.807319 |                     0 |                     3 |               1.2549  |                       1 |             0.868174 |                    0 |                    3 |                     1634.29 |                           477 |                    3289.63 |                          4 |                      15786 |
| Experimental (Sprint 3-4) |                             15.5776 |                              0.746667 |                            34.2043 |                         0.00416667 |                            142.546 |               0.293478 |                        0 |              0.565259 |                     0 |                     2 |               2.57609 |                       2 |             2.15465  |                    0 |                   12 |                     1425.38 |                           226 |                    3890.06 |                          0 |                      22983 |

## 2. Testes de Hipótese (Baseline vs Experimental)

### Time to Merge (Hours)
- Normalidade (Shapiro-Wilk): Baseline (p=0.0000), Experimental (p=0.0000) -> Não Normal
- **Teste t de Student**: p=3.0296e-03
- **Mann-Whitney U**: p=1.4529e-03
- **Cohen's d**: 0.6657

**Conclusão**: Diferença estatisticamente **SIGNIFICATIVA** (Mann-Whitney U, p < 0.05).
Houve uma **REDUÇÃO** na métrica na fase experimental.

### Comments
- Normalidade (Shapiro-Wilk): Baseline (p=0.0000), Experimental (p=0.0000) -> Não Normal
- **Teste t de Student**: p=1.7882e-03
- **Mann-Whitney U**: p=4.5665e-04
- **Cohen's d**: 0.6236

**Conclusão**: Diferença estatisticamente **SIGNIFICATIVA** (Mann-Whitney U, p < 0.05).
Houve uma **REDUÇÃO** na métrica na fase experimental.

### Reviews
- Normalidade (Shapiro-Wilk): Baseline (p=0.0000), Experimental (p=0.0000) -> Não Normal
- **Teste t de Student**: p=8.3986e-07
- **Mann-Whitney U**: p=3.4312e-06
- **Cohen's d**: -0.7313

**Conclusão**: Diferença estatisticamente **SIGNIFICATIVA** (Mann-Whitney U, p < 0.05).
Houve uma **AUMENTO** na métrica na fase experimental.

### Total Changes
- Normalidade (Shapiro-Wilk): Baseline (p=0.0000), Experimental (p=0.0000) -> Não Normal
- **Teste t de Student**: p=7.3416e-01
- **Mann-Whitney U**: p=2.4135e-01
- **Cohen's d**: 0.0566

**Conclusão**: Diferença estatisticamente **NÃO SIGNIFICATIVA** (Mann-Whitney U, p < 0.05).

## 3. Detecção de Outliers

PRs Anômalos identificados (> 3 desvios padrão):
- PR #50 (PDS-Farmvet/backend): Time to Merge (Hours) = 285.15 (Z-score > 3)
- PR #40 (PDS-Farmvet/frontend): Time to Merge (Hours) = 262.54 (Z-score > 3)
- PR #32 (PDS-Farmvet/frontend): Time to Merge (Hours) = 217.15 (Z-score > 3)
- PR #66 (PDS-Farmvet/backend): Comments = 3.00 (Z-score > 3)
- PR #49 (PDS-Farmvet/frontend): Comments = 3.00 (Z-score > 3)
- PR #149 (PDS-Farmvet/backend): Reviews = 12.00 (Z-score > 3)
- PR #147 (PDS-Farmvet/backend): Reviews = 9.00 (Z-score > 3)
- PR #110 (PDS-Farmvet/backend): Reviews = 12.00 (Z-score > 3)
- PR #76 (PDS-Farmvet/frontend): Reviews = 9.00 (Z-score > 3)
- PR #132 (PDS-Farmvet/backend): Total Changes = 22217.00 (Z-score > 3)
- PR #100 (PDS-Farmvet/backend): Total Changes = 15237.00 (Z-score > 3)
- PR #82 (PDS-Farmvet/backend): Total Changes = 14927.00 (Z-score > 3)
- PR #78 (PDS-Farmvet/frontend): Total Changes = 22983.00 (Z-score > 3)
- PR #51 (PDS-Farmvet/frontend): Total Changes = 15786.00 (Z-score > 3)

## 4. Correlações
|                       |   Time to Merge (Hours) |   Comments |    Reviews |   Total Changes |
|:----------------------|------------------------:|-----------:|-----------:|----------------:|
| Time to Merge (Hours) |               1         |  0.271204  | -0.0349993 |       0.170698  |
| Comments              |               0.271204  |  1         | -0.0568717 |      -0.073433  |
| Reviews               |              -0.0349993 | -0.0568717 |  1         |       0.0332603 |
| Total Changes         |               0.170698  | -0.073433  |  0.0332603 |       1         |

- Correlação entre Comentários e Tempo de Merge: 0.2712
- Correlação entre Tamanho do PR e Tempo de Merge: 0.1707

## 5. Segmentação

### Por Tamanho do PR
|                                                  |   count |     mean |    median |
|:-------------------------------------------------|--------:|---------:|----------:|
| ('Baseline (Sprint 1-2)', 'Grande (>500)')       |      25 | 75.1443  | 17.8275   |
| ('Baseline (Sprint 1-2)', 'Médio (100-500)')     |      13 | 26.2471  | 15.1392   |
| ('Baseline (Sprint 1-2)', 'Pequeno (<100)')      |      13 | 39.2565  |  1.60194  |
| ('Experimental (Sprint 3-4)', 'Grande (>500)')   |      32 | 26.8625  |  3.92736  |
| ('Experimental (Sprint 3-4)', 'Médio (100-500)') |      28 | 17.5002  |  0.520139 |
| ('Experimental (Sprint 3-4)', 'Pequeno (<100)')  |      32 |  2.61038 |  0.381806 |