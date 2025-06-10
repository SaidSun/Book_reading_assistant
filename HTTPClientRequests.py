import requests
import os
import re
SERVER_URL = "http://127.0.0.1:8000"

def GET_audio(file_path):
    with open(f"{file_path}.txt", "rb") as f:
        files = {"file": (f"{file_path}.txt", f)}
        response =requests.post(f"{SERVER_URL}/upload", files=files)

    if not(response.status_code == 200):
        return {"POST_request": False, "GET_request": False}
    
    response = requests.get(f"{SERVER_URL}/download/{file_path}")
    
    if response.status_code == 200:
        # if os.path.exists("{file_path}.wav"):
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            filename_regex = r"filename[^;=\n]*=((['""']).*?\2|[^;\n]*)"
            matches = re.search(filename_regex, content_disposition)
            if matches != None and matches.group(1):
                filename = matches.group(1).replace("\"", "").replace("'", "")
                print('Имя файла из Content-Disposition:', filename)
        if not(filename == "{file_path}_error"):
            with open("{file_path}.wav", "wb") as f:
                f.write(response.content)
            return {"POST_request": True, "GET_request": True}    
    return {"POST_request": True, "GET_request": False}


def GET_Modules():
    response = requests.get(f"{SERVER_URL}/settings/modules")
    if response.status_code == 200:
        return response.json()
    return None

def POST_Modules(module_name: str):
    chosen_module = {"module_name": module_name}
    response =requests.post(f"{SERVER_URL}/select/module", json=chosen_module)
    if response.status_code == 200:
        return True
    return False
