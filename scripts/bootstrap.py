#!/usr/bin/env python3
import sys
import os
import subprocess
import json
import glob

def run_git(args):
    try:
        result = subprocess.run(['git'] + args, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git error running {' '.join(args)}: {e.stderr.strip()}", file=sys.stderr)
        raise e

def check_repo_status():
    print("Checking repository status...", file=sys.stderr)
    try:
        # Fetch origin
        run_git(['fetch', 'origin'])
    except Exception:
        print("Warning: Could not fetch from origin. Proceeding with local cache check.", file=sys.stderr)

    try:
        # Get current branch name
        current_branch = run_git(['branch', '--show-current'])
        if not current_branch:
            print("Error: Not on any branch (detached HEAD).", file=sys.stderr)
            sys.exit(1)
            
        # Get upstream tracking branch
        try:
            upstream = run_git(['rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}'])
        except Exception:
            # If no upstream branch is set, check if origin/<current_branch> exists
            try:
                run_git(['rev-parse', '--verify', f'origin/{current_branch}'])
                upstream = f'origin/{current_branch}'
                print(f"No upstream tracking branch set. Defaulting to compare with {upstream}", file=sys.stderr)
            except Exception:
                print(f"No remote tracking branch found for {current_branch}. Assuming up to date.", file=sys.stderr)
                return

        # Check if behind upstream
        behind_count = int(run_git(['rev-list', '--count', f'HEAD..{upstream}']))
        ahead_count = int(run_git(['rev-list', '--count', f'{upstream}..HEAD']))

        if behind_count > 0:
            print(f"Error: Local branch '{current_branch}' is behind '{upstream}' by {behind_count} commit(s).", file=sys.stderr)
            print("Please pull the latest changes before starting.", file=sys.stderr)
            sys.exit(1)
        elif ahead_count > 0:
            print(f"Success: Local branch '{current_branch}' is ahead of '{upstream}' by {ahead_count} commit(s).", file=sys.stderr)
        else:
            print(f"Success: Local branch '{current_branch}' is up to date with '{upstream}'.", file=sys.stderr)
            
    except Exception as e:
        print(f"Error checking repository status: {e}", file=sys.stderr)
        sys.exit(1)

def load_agents(repo_root):
    agents_dir = os.path.join(repo_root, '.agents', 'agents')
    if not os.path.isdir(agents_dir):
        print(f"Error: Agents directory not found at {agents_dir}", file=sys.stderr)
        sys.exit(1)

    agents = []
    agent_paths = glob.glob(os.path.join(agents_dir, '*', 'agent.json'))
    for path in sorted(agent_paths):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            
            name = data.get('name')
            description = data.get('description', '')
            custom_agent = data.get('config', {}).get('customAgent', {})
            
            # Reconstruct system prompt
            system_prompt_sections = custom_agent.get('systemPromptSections', [])
            system_prompt_parts = []
            for sec in system_prompt_sections:
                title = sec.get('title', '')
                content = sec.get('content', '')
                system_prompt_parts.append(f"# {title}\n\n{content}")
            system_prompt = "\n\n".join(system_prompt_parts)
            
            # Determine tools based on toolNames
            tool_names = custom_agent.get('toolNames', [])
            
            enable_subagent_tools = any(t in tool_names for t in ["define_subagent", "invoke_subagent", "manage_subagents"])
            enable_write_tools = any(t in tool_names for t in ["multi_replace_file_content", "replace_file_content", "write_to_file", "run_command"])
            enable_mcp_tools = "call_mcp_tool" in tool_names
            
            agents.append({
                "name": name,
                "description": description,
                "system_prompt": system_prompt,
                "enable_subagent_tools": enable_subagent_tools,
                "enable_write_tools": enable_write_tools,
                "enable_mcp_tools": enable_mcp_tools
            })
        except Exception as e:
            print(f"Error loading agent configuration at {path}: {e}", file=sys.stderr)
            sys.exit(1)
            
    return agents

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    
    check_repo_status()
    
    agents = load_agents(repo_root)
    print(json.dumps(agents, indent=2))

if __name__ == '__main__':
    main()
