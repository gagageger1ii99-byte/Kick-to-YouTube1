import os
import argparse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_youtube(file_path, title="Uploaded Video"):
    # قراءة التوكن من الـ Environment Variables (الذي خزناه في GitHub Secrets)
    token_json = os.environ.get("YOUTUBE_TOKEN_JSON")
    if not token_json:
        raise Exception("YOUTUBE_TOKEN_JSON is not set in environment variables!")
    
    # بناء الاعتماديات
    import json
    token_info = json.loads(token_json)
    creds = Credentials.from_authorized_user_info(token_info)
    
    youtube = build('youtube', 'v3', credentials=creds)

    body = {
        'snippet': {
            'title': title,
            'description': 'تم النشر تلقائياً عبر نظام الأتمتة الخاص بنا',
            'categoryId': '22' # فئة الألعاب أو الترفيه
        },
        'status': {
            'privacyStatus': 'private' # أو public حسب رغبتك
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    
    print("... جاري رفع الفيديو إلى يوتيوب")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"تم الرفع بنسبة: {int(status.progress() * 100)}%")

    print(f"تم النشر بنجاح! Video ID: {response.get('id')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="video.mp4", help="Path to video file")
    args = parser.parse_args()
    
    upload_to_youtube(args.file)
