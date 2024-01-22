import requests
import os


def download_files(url, path):
    headers = {
        'Authorization': f'token {os.getenv("GITHUB_ACCESS_TOKEN")}'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if isinstance(data, dict) and 'message' in data:
        print(f'Error: {data["message"]} URL: {url}')
        return

    for file_info in data:
        if file_info['type'] == 'file':
            download_url = file_info['download_url']
            file_response = requests.get(download_url, headers=headers)
            file_path = os.path.join(path, file_info['name'])

            # Write file
            with open(file_path, 'wb') as file:
                file.write(file_response.content)
            print(f'Downloaded {file_path}')
        elif file_info['type'] == 'dir':
            # Recursively handle subdirectories
            new_path = os.path.join(path, file_info['name'])
            os.makedirs(new_path, exist_ok=True)
            download_files(file_info['url'], new_path)


headers = {
    'Authorization': f'token {os.getenv("GITHUB_ACCESS_TOKEN")}'
}
# Get the latest commit SHA from the master branch
repo_url = "https://api.github.com/repos/flyteorg/flytesnacks/branches/master"
response = requests.get(repo_url, headers=headers)
data = response.json()

if 'commit' in data:
    latest_commit_sha = data['commit']['sha']
    print(f"Latest commit SHA: {latest_commit_sha}")

    # Starting URL for downloading files
    start_url = f"https://api.github.com/repos/flyteorg/flytesnacks/contents?ref={latest_commit_sha}"
    start_path = "flytesnacks"
    os.makedirs(start_path, exist_ok=True)
    download_files(start_url, start_path)
else:
    print(f"Error: Unable to fetch the latest commit. {data.get('message', '')}")
