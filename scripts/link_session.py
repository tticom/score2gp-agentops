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
        
    # Strip common branch type prefixes
    for prefix in ["refactor/", "run/", "feature/", "bugfix/", "test/", "agent/"]:
        if branch.startswith(prefix):
            branch = branch[len(prefix):]
            break

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
    import re
    if re.match(r"^\d{4}-\d{2}-\d{2}", slug):
        new_dir_name = slug
    else:
        new_dir_name = f"{today}-{slug}"
    run_dir = os.path.join(runs_base, new_dir_name)
    os.makedirs(run_dir, exist_ok=True)
    return run_dir

def get_windows_resolvable_target(link_path, target_path):
    link_path = os.path.abspath(link_path)
    target_path = os.path.abspath(target_path)
    if link_path.startswith("/mnt/") and target_path.startswith("/home/"):
        distro = "Ubuntu-24.04"
        rel_path = os.path.relpath(target_path, "/")
        unc_target = f"\\\\wsl.localhost\\{distro}\\{rel_path}"
        return unc_target.replace("/", "\\")
    return target_path

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
    print(f"Synchronizing session {session_dir} <-> {run_dir}")
    
    files_to_sync = ["implementation_plan.md", "task.md", "walkthrough.md"]
    
    for filename in files_to_sync:
        session_file = os.path.join(session_dir, filename)
        repo_file = os.path.join(run_dir, filename)
        
        # Clean up symlink if it exists
        if os.path.islink(session_file):
            print(f"Removing old symlink for {filename}...")
            os.remove(session_file)
                
        session_exists = os.path.exists(session_file)
        repo_exists = os.path.exists(repo_file)
        
        if session_exists and repo_exists:
            session_mtime = os.path.getmtime(session_file)
            repo_mtime = os.path.getmtime(repo_file)
            
            # Use 1.0s threshold to avoid redundant copying due to clock skew or float precision
            if session_mtime - repo_mtime > 1.0:
                print(f"Syncing {filename}: local -> repository")
                shutil.copy2(session_file, repo_file)
            elif repo_mtime - session_mtime > 1.0:
                print(f"Syncing {filename}: repository -> local")
                shutil.copy2(repo_file, session_file)
        elif session_exists:
            print(f"Copying {filename} to repository")
            shutil.copy2(session_file, repo_file)
        elif repo_exists:
            print(f"Copying {filename} to local session")
            shutil.copy2(repo_file, session_file)

if __name__ == "__main__":
    main()
