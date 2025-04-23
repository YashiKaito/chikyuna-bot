import os
import json
from pydrive2.auth import ServiceAccountCredentials, GoogleAuth
from pydrive2.drive import GoogleDrive

# JSON認証情報を書き出し
with open("gdrive_credentials.json", "w", encoding="utf-8") as f:
    f.write(os.getenv("GDRIVE_CREDENTIALS_JSON"))

# サービスアカウントで認証
gauth = GoogleAuth()
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "gdrive_credentials.json",
    scopes=["https://www.googleapis.com/auth/drive"]
)
drive = GoogleDrive(gauth)

# Driveにアップロードするファイル一覧
files_to_upload = ["weekly_fan_score.csv", "total_fan_score.csv"]
folder_id = os.getenv("GDRIVE_FOLDER_ID")

for filename in files_to_upload:
    if not os.path.exists(filename):
        print(f"⚠️ ファイルが存在しません: {filename}")
        continue

    file = drive.CreateFile({
        "title": filename,
        "parents": [{"id": folder_id}]
    })
    file.SetContentFile(filename)
    file.Upload()
    print(f"✅ アップロード完了: {filename}")
