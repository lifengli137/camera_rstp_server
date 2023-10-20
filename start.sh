#!/bin/bash  

# Problem to be solved: the RTSP stream of the camera is active only during a test mode or motion-triggered events; thus, the stream is not continuously available; and, the stream may become unavailable anytime.  
# Method to solve the problem: 7x24 continuously tries to pull the state of the RTSP stream; if the stream is active, immediately reads through the stream and write to disk until the stream becomes unavailable again.  
# Some requirements:  
# 1. 7x24 pull and check the RTSP stream url to see if it's active.  
#   a. If it's closed, do nothing and sleep 1 second.  
#   b. If it's active, start to read until the RTSP stream URL is closed.  
#     i. Be careful of handling the RTSP stream closed suddently that make sure no data loss.  
# 2. Save the video to mp4 format and keep original quality and resolution.  
# 3. Support multiple cameras that we can define each camera's name and rstp url.  
# 4. Handle exceptions to reduce resource leaking.  
# 5. The script accepts the camera_name, its RTSP_URL, and the output_path as arguments  
# 6. The script manages the output path as hierarchy: output_path/camera_name/year/month/day/  
# 7. Only print to the STDOUT if video successfully read and written. The format of print: Name_file File_size(in MB)  
# 8. Prevent generated file gets corrupted after the RTSP stream closed suddently.  
# 9. Prevent generated empty files.  


camera_name="$1"  
rtsp_url="$2"  
output_path="$3"  
  
if [ -z "$camera_name" ] || [ -z "$rtsp_url" ] || [ -z "$output_path" ]; then  
    echo "Usage: $0 camera_name rtsp_url output_path"  
    exit 1  
fi  
  
while true; do  
    current_time=$(date +"%Y-%m-%d_%H-%M-%S")  
    file_path="${output_path}/${camera_name}/$(date +"%Y/%m/%d")"  
    file_name="${file_path}/${current_time}.mp4"  
  
    mkdir -p "$file_path"  
    openRTSP -4 -D 1 -B 10000000 -b 10000000 -t "$rtsp_url" > "$file_name" 2>>/dev/null  
  
    if [ -s "$file_name" ]; then  
        file_size=$(du -sh "$file_name" | cut -f1)  
        echo "${camera_name}_${current_time}.mp4	$file_size"  
    else  
        rm -f "$file_name"  
    fi  
  
    sleep 1  
done  
