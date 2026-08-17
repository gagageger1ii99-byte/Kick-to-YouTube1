import os
import subprocess
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def download_kick_video(m3u8_url, output_filename="video.mp4"):
    print("[⏳] جاري تحميل الفيديو من Kick...")
    cmd = [
        "ffmpeg", "-i", m3u8_url, "-c", "copy",
        "-bsf:a", "aac_adtstoasc", output_filename
    ]
    subprocess.run(cmd, check=True)
    print("[✅] تم التحميل بنجاح!")
    return output_filename

def upload_to_youtube(file_path, title, description):
    print("[⏳] جاري المصادقة ورفع الفيديو إلى يوتيوب...")
    # استخدام التوكن المحفوظ مباشرة لتجنب طلب تسجيل الدخول اليدوي
    creds = Credentials.from_authorized_user_file('token.json', ["https://www.googleapis.com/auth/youtube.upload"])
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["Kick", "Stream"],
            "categoryId": "20"
        },
        "status": {"privacyStatus": "public"}
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"[📈] نسبة الرفع: {int(status.progress() * 100)}%")

    print(f"[🎉] تم النشر بنجاح! Video ID: {response.get('id')}")

if __name__ == "__main__":
    KICK_URL = os.environ.get("KICK_URL")
    VIDEO_TITLE = os.environ.get("VIDEO_TITLE", "Kick Live Stream")
    
    video_file = download_kick_video(KICK_URL)
    upload_to_youtube(video_file, VIDEO_TITLE, "مرفع تلقائياً عبر السحابة")

