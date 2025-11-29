import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

INPUT_FILE = "responses-da6RQuZV-01KB5R1PWAEJ1CE1QMZZRYA4FG-B7YGN6RQ5VNUCWOH3BMTJYI7.csv"
OUTPUT_REPORT = "qualitative_analysis.md"
PLOT_DIR = "docs/analysis_plots"

os.makedirs(PLOT_DIR, exist_ok=True)

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found")
        return

    df = pd.read_csv(INPUT_FILE)
    
    # Rename columns for easier access (mapping based on index or keyword matching)
    # The columns are long questions. Let's map them.
    col_map = {
        "Qual é o seu nome?": "Name",
        "Como você avalia a qualidade do feedback recebido?": "FeedbackQuality",
        "O quanto as sugestões do Copilot te ajudaram?": "CopilotHelpfulness",
        "Você sentiu que economizou tempo?": "TimeSaved",
        "Comparado ao processo tradicional, como foi sua experiência?": "Experience",
        "Você recomenda adotar permanentemente?": "Recommendation",
        "Encontrou problemas que o Copilot não identificou?": "MissedByCopilot",
        "Contexto de negócio": "Missed_Business",
        "Arquitetura/design": "Missed_Arch",
        "UX/produto": "Missed_UX"
    }
    
    # Fuzzy rename or just use index if consistent
    # Let's use a loop to find columns containing keywords
    new_cols = {}
    for col in df.columns:
        for k, v in col_map.items():
            if k in col:
                new_cols[col] = v
                break
    
    df = df.rename(columns=new_cols)
    
    report = []
    report.append("## Análise Qualitativa (Survey)")
    report.append(f"**Total de Respondentes:** {len(df)}")
    
    # 1. Experience
    exp_counts = df["Experience"].value_counts()
    report.append("\n### Experiência Geral")
    report.append(exp_counts.to_markdown())
    
    # Plot Experience
    plt.figure(figsize=(8, 5))
    sns.countplot(y="Experience", data=df, palette="viridis")
    plt.title("Experiência Comparada ao Tradicional")
    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/qual_experience.png")
    plt.close()

    # 2. Time Saved
    time_counts = df["TimeSaved"].value_counts()
    report.append("\n### Economia de Tempo Percebida")
    report.append(time_counts.to_markdown())
    
    # Plot Time Saved
    plt.figure(figsize=(8, 5))
    sns.countplot(y="TimeSaved", data=df, palette="Blues")
    plt.title("Percepção de Economia de Tempo")
    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/qual_time_saved.png")
    plt.close()

    # 3. Copilot Helpfulness (1-5)
    # Assuming it's numeric
    avg_help = df["CopilotHelpfulness"].mean()
    report.append(f"\n### Utilidade do Copilot (1-5)")
    report.append(f"**Média:** {avg_help:.2f}")
    
    # 4. Recommendation
    rec_counts = df["Recommendation"].value_counts()
    report.append("\n### Recomendação de Adoção")
    report.append(rec_counts.to_markdown())
    
    # 5. What Copilot Missed (Aggregation of columns if they are checkboxes spread across cols or multi-select)
    # Looking at the CSV, it seems "Contexto de negócio", "Arquitetura/design" are separate columns with values?
    # Or maybe it's a multi-select split into columns?
    # Let's look at the raw csv again.
    # Line 1: ...,Contexto de negócio,Arquitetura/design,UX/produto,...
    # Line 2: ...,,,,... (empty)
    # Line 5: ...,Contexto de negócio,,...
    # It seems these are boolean/presence columns for "What it missed".
    # Let's count non-nulls in these specific columns if they exist.
    
    missed_cols = ["Contexto de negócio", "Arquitetura/design", "UX/produto", "Bugs lógicos", "Segurança"]
    missed_counts = {}
    for col in missed_cols:
        if col in df.columns:
            missed_counts[col] = df[col].notna().sum()
            
    report.append("\n### O que o Copilot deixou passar (Pontos de Atenção)")
    for k, v in missed_counts.items():
        report.append(f"- {k}: {v} menções")

    # Save report
    with open(OUTPUT_REPORT, "w") as f:
        f.write("\n".join(report))
        
    print(f"Qualitative analysis saved to {OUTPUT_REPORT}")

if __name__ == "__main__":
    main()
