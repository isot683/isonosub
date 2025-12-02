import sys
from datetime import datetime, timedelta
from kickapi import KickAPI
from rich.console import Console
from rich.panel import Panel
import cloudscraper

def choose_quality():
    print("\n🎦 Yayın Kalitesi Seç\n")
    choices = ["Auto","1080p60","720p60","480p30","360p30","160p30"]

    for i, c in enumerate(choices, 1):
        print(f"{i}) {c}")

    while True:
        try:
            s = int(input("\nSeçim: "))
            if 1 <= s <= len(choices):
                return choices[s-1]
        except:
            pass
        print("❌ Geçersiz seçim")

class KickStreamFinder:
    def __init__(self):
        self.session = cloudscraper.CloudScraper()
        self.console = Console()
        self.api = KickAPI()

    def get_stream(self, video_url, quality):
        parts = video_url.split("/")
        if len(parts) < 6:
            return None

        channel = parts[3]
        slug = parts[5]

        chan = self.api.channel(channel)

        for vid in chan.videos:
            if vid.uuid == slug:
                thumb = vid.thumbnail["src"]
                t = datetime.strptime(vid.start_time, "%Y-%m-%d %H:%M:%S")

                p = thumb.split("/")
                cid = p[4]
                vid_id = p[5]

                bases = [
                    "https://stream.kick.com/ivs/v1/196233775518",
                    "https://stream.kick.com/3c81249a5ce0/ivs/v1/196233775518",
                    "https://stream.kick.com/0f3cb0ebce7/ivs/v1/196233775518"
                ]

                for off in range(-5, 6):
                    tt = t + timedelta(minutes=off)

                    for base in bases:
                        if quality.lower() == "auto":
                            url = f"{base}/{cid}/{tt.year}/{tt.month}/{tt.day}/{tt.hour}/{tt.minute}/{vid_id}/media/hls/master.m3u8"
                        else:
                            url = f"{base}/{cid}/{tt.year}/{tt.month}/{tt.day}/{tt.hour}/{tt.minute}/{vid_id}/media/hls/{quality}/playlist.m3u8"

                        try:
                            if self.session.head(url, timeout=4).status_code == 200:
                                return url
                        except:
                            continue

        return None

link = input("Kick video linki: ")
quality = choose_quality()

stream = KickStreamFinder().get_stream(link, quality)

if not stream:
    print("\n❌ Yayın bulunamadı")
else:
    print("\n✅ STREAM LINK:\n")
    print(stream)
