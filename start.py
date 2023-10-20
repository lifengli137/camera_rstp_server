import ffmpeg  
import time  
import os  
import sys  
from datetime import datetime  
  
# Time interval (in seconds) to wait before retrying to connect to the RTSP stream  
RETRY_INTERVAL = 1  
  
# Format for the timestamp in the output video file name  
TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"  
  
  
def record_stream(camera_name, rtsp_url, output_base_path, time_format):  
    try:  
        # Create a timestamp and set the output video file name  
        timestamp = datetime.now().strftime(time_format)  
        output_path = os.path.join(output_base_path, camera_name, timestamp[:10].replace('-', os.sep))  
        os.makedirs(output_path, exist_ok=True)  
        output_file = os.path.join(output_path, f"{timestamp}.mp4")  
  
        # Use FFmpeg to record video and audio from the RTSP stream  
        stream = ffmpeg.input(rtsp_url)  
        stream = ffmpeg.output(stream, output_file, format='mp4', vcodec='copy', acodec='copy')  
        ffmpeg.run(stream, overwrite_output=True)  
  
        # Print the file name and size  
        file_size = os.path.getsize(output_file)  
        print(f"{output_file}\t{file_size}")  
  
    except Exception as e:  
        pass  # Silently handle exceptions to avoid interrupting the recording loop  
  
  
def main(camera_name, rtsp_url, output_path):  
    # Continuously try to record the stream  
    while True:  
        record_stream(camera_name, rtsp_url, output_path, TIME_FORMAT)  
        # Wait for the specified interval before retrying  
        time.sleep(RETRY_INTERVAL)  
  
  
if __name__ == "__main__":  
    if len(sys.argv) != 4:  
        print("Usage: python script.py <camera_name> <rtsp_url> <output_path>")  
        sys.exit(1)  
  
    camera_name = sys.argv[1]  
    rtsp_url = sys.argv[2]  
    output_path = sys.argv[3]  
    main(camera_name, rtsp_url, output_path)  
