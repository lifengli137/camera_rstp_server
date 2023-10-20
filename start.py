import cv2  
import time  
import os  
import sys  
from datetime import datetime  
  
# Time interval (in seconds) to wait before retrying to connect to the RTSP stream  
RETRY_INTERVAL = 1  
  
# Format for the timestamp in the output video file name  
TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"  
  
  
def record_stream(camera_name, rtsp_url, output_base_path, time_format):  
    cap = None  
    out = None  
  
    try:  
        # Connect to the RTSP stream  
        cap = cv2.VideoCapture(rtsp_url)  
  
        # If the connection is interrupted, print a message and return  
        if not cap.isOpened():  
            return  
  
        # Get the properties of the RTSP stream  
        fps = int(cap.get(cv2.CAP_PROP_FPS))  
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
  
        # Create a timestamp and set the output video file name  
        timestamp = datetime.now().strftime(time_format)  
        output_path = os.path.join(output_base_path, camera_name, timestamp[:10].replace('-', os.sep))  
        os.makedirs(output_path, exist_ok=True)  
        output_file = os.path.join(output_path, f"{timestamp}.mp4")  
  
        # Initialize the video writer with the stream properties  
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))  
  
        # Continuously read frames from the stream while the connection is active  
        while cap.isOpened():  
            ret, frame = cap.read()  
            if ret:  
                # Write the frame to the output video file  
                out.write(frame)  
            else:  
                # If the frame is not available (stream interrupted), break the loop  
                break  
  
        # Print the file name and size  
        file_size = os.path.getsize(output_file)  
        print(f"{output_file}\t{file_size}")  
  
    except Exception as e:  
        pass  # Silently handle exceptions to avoid interrupting the recording loop  
  
    finally:  
        # Release the resources (stream and video writer) in the finally block  
        if cap is not None:  
            cap.release()  
        if out is not None:  
            out.release()  
  
  
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
