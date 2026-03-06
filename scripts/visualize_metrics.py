import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import numpy as np

# Configuration
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
INPUT_FILE = os.path.join(BASE_DIR, "data", "pr_metrics_analyzed.csv")
PLOT_DIR = os.path.join(BASE_DIR, "results", "analysis_plots")
DASHBOARD_FILE = os.path.join(BASE_DIR, "results", "metrics_dashboard.html")

os.makedirs(PLOT_DIR, exist_ok=True)

def load_data():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return None
    return pd.read_csv(INPUT_FILE)

def save_plot(filename):
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, filename), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {filename}")

def visual_1_box_plot(df):
    """1. Gráfico Comparativo Principal: Box plot lado a lado"""
    plt.figure(figsize=(10, 6))
    
    # Calculate median reduction
    medians = df.groupby("Phase")["Time to Merge (Hours)"].median()
    baseline_med = medians.get("Baseline (Sprint 1-2)", 0)
    exp_med = medians.get("Experimental (Sprint 3-4)", 0)
    reduction = ((baseline_med - exp_med) / baseline_med) * 100 if baseline_med > 0 else 0
    
    sns.boxplot(x="Phase", y="Time to Merge (Hours)", data=df, palette=["#3498db", "#2ecc71"])
    
    # Add horizontal lines for medians
    # plt.axhline(y=baseline_med, color='blue', linestyle='--', alpha=0.5)
    # plt.axhline(y=exp_med, color='green', linestyle='--', alpha=0.5)
    
    plt.title("Impacto do Copilot no Ciclo de PRs\nTempo até Merge (Horas)", fontsize=14, fontweight='bold')
    plt.ylabel("Horas", fontsize=12)
    plt.xlabel("")
    
    # Annotate
    plt.text(0.5, df["Time to Merge (Hours)"].max() * 0.9, 
             f"Redução de {reduction:.1f}% na Mediana", 
             horizontalalignment='center', fontsize=12, color='darkgreen', weight='bold',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='green'))
    
    plt.text(0.5, -0.15, "Sprint 3-4: Revisão automatizada com GitHub Copilot", 
             horizontalalignment='center', fontsize=10, transform=plt.gca().transAxes, style='italic')
    
    save_plot("01_impacto_tempo_merge.png")

def visual_2_summary_cards(df):
    """2. Métricas Resumidas (card-style) - Saved as an image"""
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('off')
    
    # Calculate deltas
    baseline = df[df["Phase"] == "Baseline (Sprint 1-2)"]
    experimental = df[df["Phase"] == "Experimental (Sprint 3-4)"]
    
    # Time
    t_base = baseline["Time to Merge (Hours)"].median()
    t_exp = experimental["Time to Merge (Hours)"].median()
    t_delta = ((t_exp - t_base) / t_base) * 100
    
    # Comments
    c_base = baseline["Comments"].mean()
    c_exp = experimental["Comments"].mean()
    c_delta = ((c_exp - c_base) / c_base) * 100
    
    # Volume
    v_base = len(baseline)
    v_exp = len(experimental)
    
    # Semantic Adherence (calculated in previous step, let's approx here or just use what we have)
    # We'll use "Fix Rate" as a proxy for "Quality/Detection" or just Volume
    
    metrics = [
        ("Tempo Mediano (Merge)", f"{t_exp:.1f}h", f"{t_delta:.1f}%", "down"),
        ("Comentários/PR", f"{c_exp:.1f}", f"{c_delta:.1f}%", "down"),
        ("Volume de PRs", f"{v_exp}", f"vs {v_base}", "neutral"),
        ("Fase", "Experimental", "Sprint 3-4", "neutral")
    ]
    
    # Draw cards
    for i, (title, value, delta, direction) in enumerate(metrics):
        x = i * 0.25
        rect = plt.Rectangle((x + 0.01, 0.1), 0.23, 0.8, color='#f8f9fa', ec='#dee2e6', transform=ax.transAxes)
        ax.add_patch(rect)
        
        ax.text(x + 0.125, 0.7, title, ha='center', va='center', fontsize=10, color='#6c757d', transform=ax.transAxes)
        ax.text(x + 0.125, 0.5, value, ha='center', va='center', fontsize=20, weight='bold', color='#212529', transform=ax.transAxes)
        
        color = 'green' if (direction == 'down' and 'Tempo' in title) or (direction == 'down' and 'Comentários' in title) else 'gray'
        if direction == 'down': arrow = "↓"
        elif direction == 'up': arrow = "↑"
        else: arrow = ""
        
        ax.text(x + 0.125, 0.3, f"{arrow} {delta}", ha='center', va='center', fontsize=12, color=color, weight='bold', transform=ax.transAxes)

    save_plot("02_metricas_resumidas.png")

def visual_3_temporal(df):
    """3. Análise Temporal"""
    plt.figure(figsize=(12, 6))
    
    # Convert 'Merged At' to datetime if not already
    df['Merged At'] = pd.to_datetime(df['Merged At'])
    df = df.sort_values('Merged At')
    
    # Scatter
    sns.scatterplot(x="Merged At", y="Time to Merge (Hours)", hue="Phase", data=df, palette=["#3498db", "#2ecc71"], alpha=0.6)
    
    # Trend lines
    # We need numeric dates for regression
    import matplotlib.dates as mdates
    df['date_ordinal'] = df['Merged At'].map(pd.Timestamp.toordinal)
    
    for phase, color in [("Baseline (Sprint 1-2)", "#3498db"), ("Experimental (Sprint 3-4)", "#2ecc71")]:
        phase_data = df[df["Phase"] == phase]
        if len(phase_data) > 1:
            sns.regplot(x="date_ordinal", y="Time to Merge (Hours)", data=phase_data, scatter=False, color=color, line_kws={"linestyle": "--"})
    
    # Vertical line for experiment start
    # Approx split point
    split_date = df[df["Phase"] == "Experimental (Sprint 3-4)"]["Merged At"].min()
    plt.axvline(x=split_date, color='red', linestyle=':', linewidth=2, label='Início Copilot')
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    plt.title("Evolução do Tempo de Merge por Sprint", fontsize=14)
    plt.xticks(rotation=45)
    plt.legend()
    
    save_plot("03_analise_temporal.png")

def visual_4_comments(df):
    """4. Distribuição de Comentários (Total)"""
    plt.figure(figsize=(10, 6))
    
    # Histogram/KDE
    sns.histplot(data=df, x="Comments", hue="Phase", element="step", stat="density", common_norm=False, palette=["#3498db", "#2ecc71"])
    
    plt.title("Distribuição de Comentários por PR", fontsize=14)
    plt.xlabel("Número de Comentários")
    
    save_plot("04_distribuicao_comentarios.png")

def visual_5_correlation(df):
    """5. Matriz de Correlação"""
    plt.figure(figsize=(8, 6))
    
    cols = ["Time to Merge (Hours)", "Comments", "Reviews", "Total Changes", "Additions", "Deletions"]
    corr = df[cols].corr()
    
    sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f")
    plt.title("Matriz de Correlação de Métricas", fontsize=14)
    
    save_plot("05_correlacao.png")

def visual_6_devs(df):
    """6. Análise por Desenvolvedor"""
    # Clean author if needed (assuming it's cleaned in step 2 or we clean here)
    def get_login(val):
        if isinstance(val, str) and '{' in val:
            try:
                import ast
                d = ast.literal_eval(val)
                return d.get('login', 'unknown')
            except:
                return val
        return val
    
    if 'Author_Login' not in df.columns:
        if 'Author' in df.columns:
            df['Author_Login'] = df['Author'].apply(get_login)
        else:
            print("Author column not found, skipping visual_6_devs")
            return
    
    # Filter top authors
    top_authors = df['Author_Login'].value_counts().head(6).index
    dev_df = df[df['Author_Login'].isin(top_authors)]
    
    g = sns.FacetGrid(dev_df, col="Author_Login", col_wrap=3, sharey=False)
    g.map(sns.barplot, "Phase", "Time to Merge (Hours)", order=["Baseline (Sprint 1-2)", "Experimental (Sprint 3-4)"], palette=["#3498db", "#2ecc71"])
    
    g.set_titles("{col_name}")
    g.set_axis_labels("", "Horas (Média)")
    plt.subplots_adjust(top=0.9)
    g.fig.suptitle("Tempo Médio de Merge por Desenvolvedor", fontsize=14)
    
    save_plot("06_analise_devs.png")

def create_dashboard(df):
    """7. Dashboard HTML Interativo (Plotly)"""
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=("Tempo de Merge (Box Plot)", "Evolução Temporal", 
                        "Comentários por Fase", "Tamanho do PR vs Tempo",
                        "Métricas por Autor", "Correlação (Heatmap)"),
        specs=[[{}, {}], [{}, {}], [{"colspan": 2}, None]]
    )
    
    # 1. Box Plot
    fig.add_trace(go.Box(x=df["Phase"], y=df["Time to Merge (Hours)"], name="Tempo Merge", boxpoints='all'), row=1, col=1)
    
    # 2. Temporal Scatter
    fig.add_trace(go.Scatter(x=df["Merged At"], y=df["Time to Merge (Hours)"], mode='markers', 
                             marker=dict(color=df["Phase"].map({"Baseline (Sprint 1-2)": "blue", "Experimental (Sprint 3-4)": "green"})),
                             text=df["Title"], name="PRs"), row=1, col=2)
    
    # 3. Comments Bar (Avg)
    avg_comments = df.groupby("Phase")["Comments"].mean().reset_index()
    fig.add_trace(go.Bar(x=avg_comments["Phase"], y=avg_comments["Comments"], name="Média Comentários"), row=2, col=1)
    
    # 4. Size vs Time
    fig.add_trace(go.Scatter(x=df["Total Changes"], y=df["Time to Merge (Hours)"], mode='markers',
                             marker=dict(color=df["Phase"].map({"Baseline (Sprint 1-2)": "blue", "Experimental (Sprint 3-4)": "green"})),
                             text=df["Title"], name="Tamanho vs Tempo"), row=2, col=2)
    
    # 5. Author Stats (Avg Time)
    if 'Author_Login' in df.columns:
        auth_stats = df.groupby(['Author_Login', 'Phase'])["Time to Merge (Hours)"].mean().reset_index()
        # We need to pivot or just plot bars. Let's do a grouped bar manually or use px and add traces
        # For simplicity in make_subplots, let's just show top authors overall
        top_auth = df.groupby('Author_Login')["Time to Merge (Hours)"].mean().sort_values(ascending=False).head(10)
        fig.add_trace(go.Bar(x=top_auth.index, y=top_auth.values, name="Tempo Médio por Autor"), row=3, col=1)

    # Layout
    fig.update_layout(height=1000, title_text="Dashboard de Métricas de PRs - FarmVet (Copilot Experiment)", showlegend=False)
    
    # Save
    fig.write_html(DASHBOARD_FILE)
    print(f"Dashboard saved to {DASHBOARD_FILE}")

def main():
    df = load_data()
    if df is None:
        return
        
    # Clean author column globally
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

    visual_1_box_plot(df)
    visual_2_summary_cards(df)
    visual_3_temporal(df)
    visual_4_comments(df)
    visual_5_correlation(df)
    visual_6_devs(df)
    create_dashboard(df)

if __name__ == "__main__":
    main()
