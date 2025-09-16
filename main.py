from datetime import datetime
from kickapi import KickAPI
from rich.console import Console
from rich.panel import Panel

console = Console()

def get_video_stream_url(video_url: str, quality: str) -> str | None:
    try:
        parts = video_url.split("/")
        channel_name = parts[3]
        video_slug = parts[5]

        kick_api = KickAPI()
        channel = kick_api.channel(channel_name)

        for video in channel.videos:
            if video.uuid == video_slug:
                thumbnail_url = video.thumbnail["src"]
                start_time = datetime.strptime(video.start_time, "%Y-%m-%d %H:%M:%S")
                path_parts = thumbnail_url.split("/")
                channel_id, video_id = path_parts[4], path_parts[5]

                stream_url = (
                    f"https://stream.kick.com/ivs/v1/196233775518/"
                    f"{channel_id}/{start_time.year}/{start_time.month}/"
                    f"{start_time.day}/{start_time.hour}/{start_time.minute}/"
                    f"{video_id}/media/hls/{quality}/playlist.m3u8"
                )
                return stream_url
        return None
    except Exception:
        return None

def main():
    video_url = input("🎥 Kick video URL gir: ").strip()

    print("\n📺 Kalite seç (yaz):")
    print("1) 1080p60\n2) 720p60\n3) 480p30\n4) 360p30\n5) 160p30")
    choice = input("Seçim: ").strip()

    qualities = {
        "1": "1080p60",
        "2": "720p60",
        "3": "480p30",
        "4": "360p30",
        "5": "160p30"
    }
    quality = qualities.get(choice, "720p60")

    stream_url = get_video_stream_url(video_url, quality)

    if stream_url:
        console.print("\n[bold green]✅ Stream URL bulundu![/bold green]\n")
        console.print(Panel(stream_url, style="bright_blue"))
    else:
        console.print("[bold red]❌ Video bulunamadı veya URL alınamadı.[/bold red]")

if __name__ == "__main__":
    main()
