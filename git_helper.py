#!/usr/bin/env python3
"""
Git management script for DroidAgent
"""

import subprocess
import sys
import os

def run_git_command(command, description=""):
    """Run a git command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        if result.returncode == 0:
            print(f"✓ {description}")
            if result.stdout.strip():
                print(f"  Output: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ {description}")
            print(f"  Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"✗ {description} - Exception: {e}")
        return False

def check_git_status():
    """Check current git status"""
    print("=== Git Status ===")
    run_git_command("git status --porcelain", "Checking for uncommitted changes")
    run_git_command("git branch -v", "Current branch info")
    run_git_command("git remote -v", "Remote repositories")
    print()

def commit_and_push(message):
    """Commit all changes and push to remote"""
    print("=== Committing and Pushing Changes ===")
    
    # Check if there are any changes
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("No changes to commit.")
        return True
    
    # Add all changes
    if not run_git_command("git add .", "Adding all changes"):
        return False
    
    # Commit changes
    commit_cmd = f'git commit -m "{message}"'
    if not run_git_command(commit_cmd, "Committing changes"):
        return False
    
    # Push to remote
    if not run_git_command("git push origin main", "Pushing to remote repository"):
        return False
    
    print("✅ Successfully committed and pushed changes!")
    return True

def pull_latest():
    """Pull latest changes from remote"""
    print("=== Pulling Latest Changes ===")
    if run_git_command("git pull origin main", "Pulling latest changes"):
        print("✅ Successfully pulled latest changes!")
        return True
    return False

def create_new_branch(branch_name):
    """Create and switch to a new branch"""
    print(f"=== Creating New Branch: {branch_name} ===")
    if run_git_command(f"git checkout -b {branch_name}", f"Creating branch {branch_name}"):
        print(f"✅ Successfully created and switched to branch {branch_name}!")
        return True
    return False

def main():
    """Main function"""
    print("🚀 DroidAgent Git Management Tool")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python git_helper.py status              - Check git status")
        print("  python git_helper.py commit \"message\"    - Commit and push changes")
        print("  python git_helper.py pull                - Pull latest changes")
        print("  python git_helper.py branch \"name\"       - Create new branch")
        print("\nExamples:")
        print("  python git_helper.py status")
        print("  python git_helper.py commit \"Add new feature\"")
        print("  python git_helper.py pull")
        print("  python git_helper.py branch \"feature-auth\"")
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        check_git_status()
    
    elif command == "commit":
        if len(sys.argv) < 3:
            print("Please provide a commit message.")
            print("Example: python git_helper.py commit \"Add new feature\"")
            return
        message = sys.argv[2]
        check_git_status()
        commit_and_push(message)
    
    elif command == "pull":
        pull_latest()
    
    elif command == "branch":
        if len(sys.argv) < 3:
            print("Please provide a branch name.")
            print("Example: python git_helper.py branch \"feature-auth\"")
            return
        branch_name = sys.argv[2]
        create_new_branch(branch_name)
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: status, commit, pull, branch")

if __name__ == "__main__":
    main()
