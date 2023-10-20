import vlc  
import os  
import sys  
import time  
from datetime import datetime  
  
def record_rtsp(camera_name, rtsp_url, output_path):  
    while True:  
        try:  
            # Initialize VLC instance and media  
            instance = vlc.Instance("--no-xlib")  
            media = instance.media_new(rtsp_url)  
  
            # Create output directory  
            date = datetime.now()  
            output_dir = os.path.join(output_path, camera_name, date.strftime("%Y/%m/%d"))  
            os.makedirs(output_dir, exist_ok=True)  
  
            # Set output file name  
            output_file = os.path.join(output_dir, f"{camera_name}_{date.strftime('%Y%m%d_%H%M%S')}.mp4")  
            media.add_option(f":sout=#transcode{{vcodec=h264,vb=0,scale=0,acodec=mp3,ab=128,channels=2,samplerate=44100}}:standard{{access=file,mux=mp4,dst='{output_file}'}}")  
  
            # Initialize VLC player  
            player = instance.media_player_new()  
            player.set_media(media)  
  
            # Start playing the stream  
            player.play()  
  
            # Check the stream state every second  
            while True:  
                state = player.get_state()  
                if state in (vlc.State.Ended, vlc.State.Error):  
                    break  
                time.sleep(1)  
  
            # Stop the player and release resources  
            player.stop()  
            player.release()  
            instance.release()  
  
            # Print the output file information  
            file_size = os.path.getsize(output_file) / (1024 * 1024)  
            print(f"{output_file}\t{file_size:.2f} MB")  
        except Exception as e:  
            print(f"Error: {e}")  
            time.sleep(1)  
  
if __name__ == "__main__":  
    if len(sys.argv) != 4:  
        print("Usage: python rtsp_recorder.py <camera_name> <rtsp_url> <output_path>")  
        sys.exit(1)  
  
    camera_name, rtsp_url, output_path = sys.argv[1], sys.argv[2], sys.argv[3]  
    record_rtsp(camera_name, rtsp_url, output_path)  
