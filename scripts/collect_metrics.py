import subprocess
import json
import pandas as pd
from datetime import datetime
import sys
import os

# Configuration
REPOS = [
    "PDS-Farmvet/backend",
    "PDS-Farmvet/frontend"
]

# Date Ranges
# Baseline: Sprint 1 (02/09-18/09) + Sprint 2 (18/09-20/10) -> Approx 02/09 to 20/10
# Experimental: Sprint 3 (20/10-03/11) + Sprint 4 (03/11-Now) -> Approx 21/10 to Now
BASELINE_START = datetime(2025, 9, 2)
BASELINE_END = datetime(2025, 10, 20)
EXPERIMENTAL_START = datetime(2025, 10, 21)
EXPERIMENTAL_END = datetime.now() # Or fixed date if needed

def run_gh_command(args):
    """Run a gh command and return the output."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running gh command: {e}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)

def get_prs(repo):
    """Fetch merged PRs from a repository."""
    print(f"Fetching PRs from {repo}...")
    # Fields: createdAt, mergedAt, comments, reviews, additions, deletions, number, url, author
    fields = "createdAt,mergedAt,comments,reviews,additions,deletions,number,url,author,title"
    # Fetch enough PRs to cover the date range. 
    # Since we filter by date later, we get a reasonable amount (e.g., last 200).
    output = run_gh_command([
        "pr", "list",
        "-R", repo,
        "--state", "merged",
        "--limit", "200",
        "--json", fields
    ])
    return json.loads(output)

def parse_date(date_str):
    """Parse GitHub date string."""
    if not date_str:
        return None
    # GitHub dates are usually ISO 8601: 2025-09-18T12:34:56Z
    return datetime.fromisoformat(date_str.replace('Z', '+00:00')).replace(tzinfo=None)

def process_prs(repos):
    all_data = []
    
    for repo in repos:
        prs = get_prs(repo)
        for pr in prs:
            merged_at = parse_date(pr.get("mergedAt"))
            created_at = parse_date(pr.get("createdAt"))
            
            if not merged_at or not created_at:
                continue
            
            # Determine Sprint/Phase
            phase = None
            if BASELINE_START <= merged_at <= BASELINE_END:
                phase = "Baseline (Sprint 1-2)"
            elif EXPERIMENTAL_START <= merged_at <= EXPERIMENTAL_END:
                phase = "Experimental (Sprint 3-4)"
            
            if not phase:
                continue
                
            # Calculate Metrics
            time_to_merge_hours = (merged_at - created_at).total_seconds() / 3600
            
            # Count review comments (reviews is a list of reviews, each might have comments? 
            # Actually 'reviews' in gh json is a list of review objects. 
            # 'reviewRequests' is different. 
            # We also have 'reviewComments' field available in gh, let's check if we requested it.
            # Wait, 'reviews' gives the list of reviews. The number of reviews is len(reviews).
            # Total comments = comments (general) + review comments (inline).
            # gh json 'comments' is a list of comments. 'reviews' is a list of reviews.
            # To get counts, we can just use the length if they are lists, or the count if they are numbers.
            # 'gh pr list --json comments' returns a list of comments.
            # Let's verify what 'comments' and 'reviews' return. 
            # Usually they return lists of objects.
            
            num_comments = len(pr.get("comments", []))
            num_reviews = len(pr.get("reviews", []))
            # Note: 'reviews' includes approvals, changes requested, etc.
            
            all_data.append({
                "Repo": repo,
                "PR": pr["number"],
                "Title": pr["title"],
                "Phase": phase,
                "Time to Merge (Hours)": time_to_merge_hours,
                "Comments": num_comments,
                "Reviews": num_reviews,
                "Additions": pr["additions"],
                "Deletions": pr["deletions"],
                "Total Changes": pr["additions"] + pr["deletions"],
                "Merged At": merged_at
            })
            
    return pd.DataFrame(all_data)

def main():
    print("Starting metric collection...")
    print(f"Baseline: {BASELINE_START.date()} to {BASELINE_END.date()}")
    print(f"Experimental: {EXPERIMENTAL_START.date()} to {EXPERIMENTAL_END.date()}")
    
    df = process_prs(REPOS)
    
    if df.empty:
        print("No PRs found in the specified date ranges.")
        return

    # Analysis
    print("\n--- Comparative Analysis ---")
    
    # Group by Phase
    summary = df.groupby("Phase")[
        ["Time to Merge (Hours)", "Comments", "Reviews", "Total Changes"]
    ].agg(['mean', 'median', 'count'])
    
    # Calculate additional metrics
    print("\n--- Advanced Metrics ---")
    for phase in df["Phase"].unique():
        phase_data = df[df["Phase"] == phase]
        total = len(phase_data)
        
        # Quality Proxy: % of PRs that are fixes
        fix_count = phase_data["Title"].str.lower().str.startswith("fix").sum()
        fix_rate = (fix_count / total) * 100
        
        # Process Adherence: % of PRs following Conventional Commits (feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert):
        # We'll do a simple check for the colon
        semantic_count = phase_data["Title"].str.match(r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+', case=False).sum()
        semantic_rate = (semantic_count / total) * 100
        
        print(f"\nPhase: {phase}")
        print(f"  Fix Rate (Bugs/Corrections): {fix_rate:.1f}% ({fix_count}/{total})")
        print(f"  Semantic PR Adherence: {semantic_rate:.1f}% ({semantic_count}/{total})")
    
    print("\n" + "="*30 + "\n")
    print(summary)
    
    # Save to CSV
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "pr_metrics_analysis.csv")
    df.to_csv(output_file, index=False)
    print(f"\nDetailed data saved to {output_file}")

if __name__ == "__main__":
    main()
