import yt_dlp
import os
import subprocess


def convert_webm_to_mp3(input_file, output_dir="."):
    """Converts a WebM audio file to MP3 using ffmpeg."""
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + ".mp3")
    try:
        subprocess.run(
            ["ffmpeg", "-i", input_file, output_file],
            check=True,
            capture_output=True
        )
        os.remove(input_file)  # Remove the original WebM
        print(f"Converted to MP3: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting to MP3: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please ensure ffmpeg is installed and in your PATH.")
        return False

def download_youtube_audio(video_url, output_dir=".", prefer_320kbps=False):
    """Downloads the audio from a YouTube video, with optional 320kbps and automatic WebM to MP3 conversion.

    Args:
      video_url: The URL of the YouTube video.
      output_dir: The directory to save the downloaded audio file in.
                  Defaults to the current directory.
       prefer_320kbps: Whether to prioritize 320 kbps audio, it defaults to False
    """
    if prefer_320kbps:
         ydl_opts = {
             'format': 'bestaudio[abr>=320]/bestaudio/best',  # Selects best audio with 320kbps or the best if not available
             'outtmpl': '%(title)s.%(ext)s',  # Output file name template
            'noplaylist': True,  # Download only the video specified, not the playlist
            'extractaudio': True,  # Only extract audio
            'cachedir': False,  # Disable cache to avoid issues
            'output': os.path.join(output_dir, '%(title)s.%(ext)s'),
         }
    else:
        ydl_opts = {
            'format': 'bestaudio/best',  # Get the best available audio format
            'outtmpl': '%(title)s.%(ext)s',  # Output file name template
            'noplaylist': True,  # Download only the video specified, not the playlist
            'extractaudio': True,  # Only extract audio
            'cachedir': False,  # Disable cache to avoid issues
            'output': os.path.join(output_dir, '%(title)s.%(ext)s'),
        }


    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)

            if info_dict:
                downloaded_file = ydl.prepare_filename(info_dict)
                print(f"Successfully downloaded: {downloaded_file}")

                if downloaded_file.lower().endswith(".webm"):  # Convert WebM to MP3
                   if convert_webm_to_mp3(downloaded_file,output_dir):
                        return
                   else:
                       print(f"Could not convert file")

                elif downloaded_file.lower().endswith(".mp3"):
                    return
                else:
                    print("Downloaded audio is not in mp3 or webm format")
            else:
                 print(f"Could not get info for {video_url}")
    except Exception as e:
          print(f"An error occurred: {e}")



if __name__ == "__main__":
    video_link = input("Enter the YouTube video link: ")
    output_directory = input("Enter the output directory (or press Enter for current directory): ")
    prefer_320kbps = input("Prefer 320 kbps quality? (y/n, default is n): ").lower() == "y"
    if not output_directory:
        output_directory = "."
    
    download_youtube_audio(video_link, output_directory, prefer_320kbps)
