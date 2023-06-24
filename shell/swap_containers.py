#!/usr/bin/env python3

 import os
 import subprocess
 import json

 def get_command(company, repo, action):
     with open('config.json') as f:
         data = json.load(f)
     try:
         return data[company][repo][action]
     except KeyError:
         return None

 def replace_containers(stop_company, start_company):
     print("Replacing containers...")

     for repo in ["frontend", "backend", "algs1", "algs2"]:
         # Stop old containers
         stop_command = get_command(stop_company, repo, "kill")
         stop_repodir = f"{stop_company}/{repo}/"

         if os.path.isdir(stop_repodir):
             print(f"Stopping {repo} in {stop_company}")
             os.chdir(stop_repodir)
             if stop_command:
                 subprocess.check_call(stop_command, shell=True)
             os.chdir("../../")
         else:
             print(f"Could not find {repo} in {stop_company}. Skipping...")

         # Start new containers
         start_command = get_command(start_company, repo, "run")
         start_repodir = f"{start_company}/{repo}/"

         if os.path.isdir(start_repodir):
             print(f"Starting {repo} in {start_company}")
             os.chdir(start_repodir)
             if start_command:
                 subprocess.check_call(start_command, shell=True)
             os.chdir("../../")
         else:
             print(f"Could not find {repo} in {start_company}. Skipping...")

     print("Container Replacement Complete!")

 if __name__ == "__main__":
     import sys
     if len(sys.argv) != 3:
         print("Usage: ./replace_containers.py <stop_company> <start_company>")
         sys.exit(1)

     stop_company, start_company = sys.argv[1], sys.argv[2]
     replace_containers(stop_company, start_company)
