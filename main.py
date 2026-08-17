import os
import argparse
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_youtube(file_path, title, privacy_status):
    token_json = os.environ.get("YOUTUBE_TOKEN_JSON")
    if not token_json:
        raise Exception("YOUTUBE_TOKEN_JSON is not set in environment variables!")
    
    token_info = json.loads(token_json)
    creds = Credentials.from_authorized_user_info(token_info)
    
    youtube = build('youtube', 'v3', credentials=creds)

    body = {
        'snippet': {
            'title': title,
            'description': 'تم النشر تلقائياً عبر نظام الأتمتة المطور 🚀',
            'categoryId': '22' # فئة الألعاب
        },
        'status': {
            'privacyStatus': privacy_status
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
            print(f"نسبة الرفع: {int(status.progress() * 100)}%")

    print(f"تم النشر بنجاح! Video ID: {response.get('id')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="video.mp4", help="Path to video file")
    parser.add_argument("--title", default="Uploaded Video", help="Video Title")
    parser.add_argument("--privacy", default="private", help="Privacy Status")
    args = parser.parse_args()
    
    upload_to_youtube(args.file, args.title, args.privacy)
