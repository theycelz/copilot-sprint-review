import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuration
INPUT_FILE = "pr_metrics_analysis.csv"
OUTPUT_REPORT = "analysis_report.md"
OUTPUT_DATA = "pr_metrics_analyzed.csv"
OUTPUT_CORR = "correlation_matrix.csv"
PLOT_DIR = "docs/analysis_plots"

os.makedirs(PLOT_DIR, exist_ok=True)

def load_data():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return None
    return pd.read_csv(INPUT_FILE)

def calculate_cohens_d(group1, group2):
    """Calculate Cohen's d for effect size."""
    diff = group1.mean() - group2.mean()
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(), group2.var()
    
    # Pooled standard deviation
    pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
    pooled_std = np.sqrt(pooled_var)
    
    return diff / pooled_std

def analyze_distribution(df, metric, phase):
    """Analyze distribution normality."""
    data = df[df["Phase"] == phase][metric].dropna()
    stat, p_value = stats.shapiro(data)
    
    # Plot
    plt.figure(figsize=(10, 6))
    sns.histplot(data, kde=True, stat="density")
    
    # Overlay normal curve
    mu, std = stats.norm.fit(data)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    
    plt.title(f"Distribution of {metric} - {phase}\nShapiro-Wilk p={p_value:.4f}")
    plt.savefig(f"{PLOT_DIR}/dist_{metric.replace(' ', '_')}_{phase.split()[0]}.png")
    plt.close()
    
    return p_value

def main():
    df = load_data()
    if df is None:
        return

    report_lines = []
    report_lines.append("# Relatório de Análise Estatística de Métricas de PRs")
    report_lines.append("\n## 1. Estatísticas Descritivas")

    # 1. Descriptive Stats
    metrics = ["Time to Merge (Hours)", "Comments", "Reviews", "Total Changes"]
    desc_stats = df.groupby("Phase")[metrics].agg(['mean', 'median', 'std', 'min', 'max'])
    report_lines.append(desc_stats.to_markdown())
    
    # 2. Hypothesis Testing
    report_lines.append("\n## 2. Testes de Hipótese (Baseline vs Experimental)")
    
    baseline = df[df["Phase"] == "Baseline (Sprint 1-2)"]
    experimental = df[df["Phase"] == "Experimental (Sprint 3-4)"]
    
    for metric in metrics:
        report_lines.append(f"\n### {metric}")
        
        # Data
        b_data = baseline[metric].dropna()
        e_data = experimental[metric].dropna()
        
        # Normality Check
        p_norm_b = analyze_distribution(df, metric, "Baseline (Sprint 1-2)")
        p_norm_e = analyze_distribution(df, metric, "Experimental (Sprint 3-4)")
        
        is_normal = p_norm_b > 0.05 and p_norm_e > 0.05
        report_lines.append(f"- Normalidade (Shapiro-Wilk): Baseline (p={p_norm_b:.4f}), Experimental (p={p_norm_e:.4f}) -> {'Normal' if is_normal else 'Não Normal'}")
        
        # Tests
        # T-Test (Parametric)
        t_stat, t_p = stats.ttest_ind(b_data, e_data, equal_var=False)
        
        # Mann-Whitney U (Non-Parametric)
        u_stat, u_p = stats.mannwhitneyu(b_data, e_data)
        
        # Effect Size
        d = calculate_cohens_d(b_data, e_data)
        
        report_lines.append(f"- **Teste t de Student**: p={t_p:.4e}")
        report_lines.append(f"- **Mann-Whitney U**: p={u_p:.4e}")
        report_lines.append(f"- **Cohen's d**: {d:.4f}")
        
        # Interpretation
        chosen_p = t_p if is_normal else u_p
        test_name = "Teste t" if is_normal else "Mann-Whitney U"
        significance = "SIGNIFICATIVA" if chosen_p < 0.05 else "NÃO SIGNIFICATIVA"
        direction = "REDUÇÃO" if d > 0 else "AUMENTO" # d = (mean1 - mean2) / s. If positive, mean1 (Baseline) > mean2 (Exp), so Reduction.
        
        report_lines.append(f"\n**Conclusão**: Diferença estatisticamente **{significance}** ({test_name}, p < 0.05).")
        if significance == "SIGNIFICATIVA":
            report_lines.append(f"Houve uma **{direction}** na métrica na fase experimental.")

    # 3. Outliers
    report_lines.append("\n## 3. Detecção de Outliers")
    df['Outlier'] = False
    outlier_reasons = []
    
    for metric in metrics:
        mean = df[metric].mean()
        std = df[metric].std()
        threshold = 3 * std
        
        outliers = df[abs(df[metric] - mean) > threshold]
        if not outliers.empty:
            df.loc[outliers.index, 'Outlier'] = True
            for idx, row in outliers.iterrows():
                df.loc[idx, f'Outlier_{metric}'] = True
                outlier_reasons.append(f"- PR #{row['PR']} ({row['Repo']}): {metric} = {row[metric]:.2f} (Z-score > 3)")

    if outlier_reasons:
        report_lines.append("\nPRs Anômalos identificados (> 3 desvios padrão):")
        report_lines.extend(outlier_reasons)
    else:
        report_lines.append("\nNenhum outlier extremo identificado (> 3 desvios padrão).")

    # 4. Correlations
    report_lines.append("\n## 4. Correlações")
    corr_matrix = df[metrics].corr()
    report_lines.append(corr_matrix.to_markdown())
    corr_matrix.to_csv(OUTPUT_CORR)
    
    # Specific check
    corr_comments_time = df["Comments"].corr(df["Time to Merge (Hours)"])
    report_lines.append(f"\n- Correlação entre Comentários e Tempo de Merge: {corr_comments_time:.4f}")
    
    corr_size_time = df["Total Changes"].corr(df["Time to Merge (Hours)"])
    report_lines.append(f"- Correlação entre Tamanho do PR e Tempo de Merge: {corr_size_time:.4f}")

    # 5. Segmentation
    report_lines.append("\n## 5. Segmentação")
    
    # By Author
    if 'Author' in df.columns: # Check if we have Author data, collect_metrics might need update if not present or if it's a dict
        # In collect_metrics.py I requested 'author' in json fields, but didn't parse it to a flat string in the dict.
        # Let's check if 'author' column exists and is usable.
        # If it's a dict/json object, we might need to extract login.
        # Actually, looking at collect_metrics.py, I did: "author": pr["author"]
        # pr["author"] is usually a dict {login: ..., ...}.
        # I should probably fix that in this script if needed.
        pass
    
    # Let's try to extract author login if it's a string representation of a dict
    try:
        # Assuming it might be loaded as a string or dict
        # But wait, I saved it to CSV. CSV saves dicts as strings.
        # I'll try to clean it up.
        def get_login(val):
            if isinstance(val, str) and '{' in val:
                try:
                    import ast
                    d = ast.literal_eval(val)
                    return d.get('login', 'unknown')
                except:
                    return val
            return val
            
        if 'Author' in df.columns:
            df['Author_Login'] = df['Author'].apply(get_login)
            author_stats = df.groupby('Author_Login')["Time to Merge (Hours)"].agg(['count', 'mean', 'median'])
            report_lines.append("\n### Por Autor (Top 5 por volume)")
            report_lines.append(author_stats.sort_values('count', ascending=False).head(5).to_markdown())
    except Exception as e:
        report_lines.append(f"\nErro na segmentação por autor: {e}")

    # By Size
    # Small < 100, Medium < 500, Large >= 500
    def categorize_size(lines):
        if lines < 100: return "Pequeno (<100)"
        if lines < 500: return "Médio (100-500)"
        return "Grande (>500)"
        
    df['Size_Category'] = df['Total Changes'].apply(categorize_size)
    size_stats = df.groupby(['Phase', 'Size_Category'])["Time to Merge (Hours)"].agg(['count', 'mean', 'median'])
    report_lines.append("\n### Por Tamanho do PR")
    report_lines.append(size_stats.to_markdown())

    # Save outputs
    with open(OUTPUT_REPORT, "w") as f:
        f.write("\n".join(report_lines))
    
    df.to_csv(OUTPUT_DATA, index=False)
    print(f"Analysis complete. Report saved to {OUTPUT_REPORT}")

    # Executive Summary for Console
    print("\n--- EXECUTIVE SUMMARY ---")
    
    # Time to Merge Result
    b_time = baseline["Time to Merge (Hours)"].dropna()
    e_time = experimental["Time to Merge (Hours)"].dropna()
    u_stat, u_p = stats.mannwhitneyu(b_time, e_time)
    
    print(f"1. O Copilot reduziu significativamente o tempo até merge? {'SIM' if u_p < 0.05 else 'NÃO'} (Mann-Whitney p={u_p:.4e})")
    print(f"   - Mediana Baseline: {b_time.median():.2f}h -> Experimental: {e_time.median():.2f}h")
    
    # Comments Result
    b_comm = baseline["Comments"].dropna()
    e_comm = experimental["Comments"].dropna()
    print(f"2. Comentários Humanos: Média de {b_comm.mean():.1f} para {e_comm.mean():.1f}")
    
    # Trade-offs
    print("3. Trade-offs: Ver relatório completo para detalhes de correlações e outliers.")

if __name__ == "__main__":
    main()
