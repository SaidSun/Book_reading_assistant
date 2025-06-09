import requests

SERVER_URL = "http://127.0.0.1:8000"

file_path = "example.txt"
# with open(file_path, "w") as f:
    # f.write("Hello, there!")

with open(file_path, "rb") as f:
    files = {"file": (file_path, f)}
    response =requests.post(f"{SERVER_URL}/upload", files=files)

print(response.json())

response = requests.get(f"{SERVER_URL}/download/example")
with open("downloaded_file.txt", "wb") as f:
    f.write(response.content)