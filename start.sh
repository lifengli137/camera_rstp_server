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
    file_name="/tmp/${camera_name}_${current_time}.mp4"  
    key_file="/tmp/${camera_name}_${current_time}.bin"

    encrypted_file="${file_path}/${current_time}.enc"  
    encrypted_key="${file_path}/${current_time}.key"  
    
    mkdir -p "$file_path"  
    timeout 600 openRTSP -4 -D 1 -B 10000000 -b 10000000 -t "$rtsp_url" > "$file_name" 2>/dev/null  
  
    if [ -s "$file_name" ]; then  
        file_size=$(du -sh "$file_name" | cut -f1)  
        echo "${camera_name}_${current_time}.mp4	$file_size"  

        openssl rand -base64 32 > ${key_file}
        openssl rsautl -encrypt -inkey ~/.ssh/id_rsa.pub.pem -pubin -in ${key_file} -out ${encrypted_key}

        openssl enc -aes-256-cbc -in ${file_name} -out ${encrypted_file} -pass file:${key_file} -salt -md md5

        
        rm -f "$key_file"
    fi
    
    rm -f "$file_name"  
    sleep 1  
done  
