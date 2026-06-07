#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

def get_active_run_dir(repo_root):
    # Determine the run directory based on current git branch in score2gp product repository
    product_repo = os.path.abspath(os.path.join(repo_root, "..", "score2gp"))
    if not os.path.exists(product_repo):
        product_repo = repo_root  # fallback
    
    try:
        branch = subprocess.check_output(
            ["git", "-C", product_repo, "rev-parse", "--abbrev-ref", "HEAD"],
            text=True
        ).strip()
    except Exception:
        branch = "main"
        
    # Standardize branch name to run slug (replace slash and underscores)
    slug = branch.replace("/", "-").replace("_", "-")
    
    # We prefix with date if possible, otherwise just use slug
    import datetime
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    # Search for an existing runs folder matching the slug
    runs_base = os.path.join(repo_root, "projects", "score2gp", "runs")
    os.makedirs(runs_base, exist_ok=True)
    
    for entry in os.listdir(runs_base):
        if entry.endswith(slug) and os.path.isdir(os.path.join(runs_base, entry)):
            return os.path.join(runs_base, entry)
            
    # Default new directory
    new_dir_name = f"{today}-{slug}"
    run_dir = os.path.join(runs_base, new_dir_name)
    os.makedirs(run_dir, exist_ok=True)
    return run_dir

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 link_session.py <session_brain_dir>", file=sys.stderr)
        sys.exit(1)
        
    session_dir = os.path.abspath(sys.argv[1])
    if not os.path.isdir(session_dir):
        print(f"Error: Session brain directory {session_dir} does not exist.", file=sys.stderr)
        sys.exit(1)
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    
    run_dir = get_active_run_dir(repo_root)
    print(f"Linking session {session_dir} -> {run_dir}")
    
    files_to_link = ["implementation_plan.md", "task.md", "walkthrough.md"]
    
    for filename in files_to_link:
        session_file = os.path.join(session_dir, filename)
        repo_file = os.path.join(run_dir, filename)
        
        # 1. If file exists locally but not in repo, move it to repo
        if os.path.exists(session_file) and not os.path.islink(session_file):
            if not os.path.exists(repo_file):
                print(f"Moving local {filename} to repository...")
                shutil.copy2(session_file, repo_file)
            os.remove(session_file)
            
        # 2. If it exists in repo but not locally, ensure local is clear
        elif os.path.exists(session_file) and os.path.islink(session_file):
            # Already a link, verify target
            try:
                target = os.readlink(session_file)
                if os.path.abspath(target) == os.path.abspath(repo_file):
                    continue
            except Exception:
                os.remove(session_file)
                
        # 3. Create symlink from session_file to repo_file
        if os.path.exists(repo_file):
            try:
                print(f"Creating symlink: {session_file} -> {repo_file}")
                # Use absolute Windows path or relative path depending on platform
                os.symlink(repo_file, session_file)
            except OSError as e:
                print(f"Warning: Could not create symlink ({e}). Falling back to file copy sync.", file=sys.stderr)
                # Fallback: copy file
                shutil.copy2(repo_file, session_file)

if __name__ == "__main__":
    main()
