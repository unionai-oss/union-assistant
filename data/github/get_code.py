import subprocess

def extract_repo_name(repo_url: str) -> str:
    # Split the URL by '/' and get the last part
    parts = repo_url.split('/')
    repo_name = parts[-1]
  
    return repo_name

repo_urls = ["https://github.com/flyteorg/flyte",
             "https://github.com/flyteorg/flytectl",
             "https://github.com/flyteorg/flytekit",
             "https://github.com/flyteorg/flyteconsole",]

for repo_url in repo_urls:
    repo_name = extract_repo_name(repo_url)
    try:
        print(f"Cloning {repo_name}...")
        subprocess.run(['git', 'clone', repo_url, f'./{repo_name}'])
        print(f"Cloned {repo_name}!")
    except :
        continue