import vlc  
import time  
import os  
import sys  
from datetime import datetime  
  
def check_rtsp_stream(rtsp_url):  
    instance = vlc.Instance("--no-xlib")  
    player = instance.media_player_new()  
    media = instance.media_new(rtsp_url)  
    player.set_media(media)  
    player.play()  
    time.sleep(1)  
  
    if player.get_state() == vlc.State.Playing:  
        player.stop()  
        return True  
    player.stop()  
    return False  
  
def save_rtsp_stream(camera_name, rtsp_url, output_path):  
    output_folder = os.path.join(output_path, camera_name, datetime.now().strftime("%Y/%m/%d"))  
    os.makedirs(output_folder, exist_ok=True)  
  
    output_file = os.path.join(output_folder, f"{camera_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")  
    instance = vlc.Instance("--no-xlib", f"--sout=#std{{access=file,mux=mp4,dst='{output_file}'}}")  
    player = instance.media_player_new()  
  
    media = instance.media_new(rtsp_url)  
    player.set_media(media)  
    player.play()  
  
    while player.get_state() != vlc.State.Ended and player.get_state() != vlc.State.Error:  
        time.sleep(1)  
  
    player.stop()  
      
    if os.path.getsize(output_file) > 0:  
        print(f"{output_file}\t{os.path.getsize(output_file) / (1024 * 1024)} MB")  
    else:  
        os.remove(output_file)  
  
def main(camera_name, rtsp_url, output_path):  
    while True:  
        try:  
            if check_rtsp_stream(rtsp_url):  
                save_rtsp_stream(camera_name, rtsp_url, output_path)  
            else:  
                time.sleep(1)  
        except Exception as e:  
            print(f"Error: {e}")  
            time.sleep(1)  
  
if __name__ == "__main__":  
    if len(sys.argv) != 4:  
        print("Usage: python script.py <camera_name> <rtsp_url> <output_path>")  
        sys.exit(1)  
  
    camera_name, rtsp_url, output_path = sys.argv[1], sys.argv[2], sys.argv[3]  
    main(camera_name, rtsp_url, output_path)  
