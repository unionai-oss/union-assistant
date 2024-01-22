import requests
import os

def download_files(url, path):
    headers = {
        'Authorization': f'token {os.getenv("GITHUB_ACCESS_TOKEN")}'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if isinstance(data, dict) and data.get('message') == 'Not Found':
        print(f'Error: URL not found {url}')
        return

    for file_info in data:
        if file_info['type'] == 'file':
            download_url = file_info['download_url']
            file_response = requests.get(download_url, headers=headers)
            file_path = os.path.join(path, file_info['name'])

            # 寫入檔案
            with open(file_path, 'wb') as file:
                file.write(file_response.content)
            print(f'Downloaded {file_path}')
        elif file_info['type'] == 'dir':
            # 遞迴處理子資料夾
            new_path = os.path.join(path, file_info['name'])
            os.makedirs(new_path, exist_ok=True)
            download_files(file_info['url'], new_path)

# 起始URL
start_url = "https://api.github.com/repos/flyteorg/flyte/contents/rfc?ref=master"
start_path = "rfc"
os.makedirs(start_path, exist_ok=True)
download_files(start_url, start_path)
