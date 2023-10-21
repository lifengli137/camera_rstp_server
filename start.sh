#!/bin/bash  

camera_name="$1"  
rtsp_url="$2"  
output_path="$3"  
pass="$4"
  
if [ -z "$camera_name" ] || [ -z "$rtsp_url" ] || [ -z "$output_path" ]; then  
    echo "Usage: $0 camera_name rtsp_url output_path"  
    exit 1  
fi  
  
while true; do  
    current_time=$(date +"%Y-%m-%d_%H-%M-%S")  
    file_path="${output_path}/${camera_name}/$(date +"%Y/%m/%d")"  
    file_name="${file_path}/${current_time}.mp4"  
    encrypted_file="${file_path}/${current_time}.enc"  

    mkdir -p "$file_path"  
    timeout 180 openRTSP -4 -D 1 -B 10000000 -b 10000000 -t "$rtsp_url" > "$file_name" 
  
    if [ -s "$file_name" ]; then  
        file_size=$(du -sh "$file_name" | cut -f1)  
        echo "${camera_name}_${current_time}.mp4	$file_size"  
        openssl enc -aes-256-cbc -in ${file_name} -out ${encrypted_file} -pass pass:${pass}${current_time} -salt -pbkdf2
    fi
      
  
    sleep 1  
done  
