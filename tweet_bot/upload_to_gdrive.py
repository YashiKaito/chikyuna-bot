import os
import json
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# シークレットから認証情報を読み込む
credentials = os.getenv("GDRIVE_CREDENTIALS_JSON")
folder_id = os.getenv("GDRIVE_FOLDER_ID")

with open("gdrive_credentials.json", "w", encoding="utf-8") as f:
    f.write(credentials)

gauth = GoogleAuth()
gauth.LoadCredentialsFile("gdrive_credentials.json")
if not gauth.credentials:
    gauth.LocalWebserverAuth()
gauth.SaveCredentialsFile("gdrive_credentials.json")

drive = GoogleDrive(gauth)

files_to_upload = ["weekly_fan_score.csv", "total_fan_score.csv"]

for filename in files_to_upload:
    if not os.path.exists(filename):
        print(f"ファイルが存在しません: {filename}")
        continue

    file = drive.CreateFile({
        "title": filename,
        "parents": [{"id": folder_id}]
    })
    file.SetContentFile(filename)
    file.Upload()
    print(f"アップロード完了: {filename}")