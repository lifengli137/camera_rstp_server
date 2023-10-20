import vlc  
import time  
import sys  
import os  
from datetime import datetime  
  
def check_stream(rtsp_url):  
    instance = vlc.Instance("--no-xlib")  
    player = instance.media_player_new()  
    media = instance.media_new(rtsp_url)  
    player.set_media(media)  
    player.play()  
    time.sleep(1)  
    return player.get_state() == vlc.State.Playing  
  
def record_stream(camera_name, rtsp_url, output_path):  
    output_path = os.path.join(output_path, camera_name)  
    os.makedirs(output_path, exist_ok=True)  
  
    while True:  
        if check_stream(rtsp_url):  
            now = datetime.now()  
            date_path = now.strftime("%Y/%m/%d")  
            output_folder = os.path.join(output_path, date_path)  
            os.makedirs(output_folder, exist_ok=True)  
  
            output_file = now.strftime("%Y%m%d_%H%M%S") + ".mp4"  
            output_file_path = os.path.join(output_folder, output_file)  
  
            instance = vlc.Instance("--no-xlib")  
            player = instance.media_player_new()  
            media = instance.media_new(rtsp_url)  
            media.add_option(f"sout=#transcode{{vcodec=h264}}:std{{access=file,dst={output_file_path}}}")  
            player.set_media(media)  
            player.play()  
  
            while player.get_state() != vlc.State.Ended:  
                time.sleep(1)  
  
            file_size = os.path.getsize(output_file_path) / (1024 * 1024)  
            print(f"{output_file}\t{file_size:.2f} MB")  
        else:  
            time.sleep(1)  
  
if __name__ == "__main__":  
    if len(sys.argv) != 4:  
        print("Usage: python script.py <camera_name> <rtsp_url> <output_path>")  
        sys.exit(1)  
  
    camera_name = sys.argv[1]  
    rtsp_url = sys.argv[2]  
    output_path = sys.argv[3]  
  
    try:  
        record_stream(camera_name, rtsp_url, output_path)  
    except Exception as e:  
        print(f"Error: {e}")  
