Problem to be solved: the RTSP stream of the camera is active only during a test mode or motion-triggered events; thus, the stream is not continuously available; and, the stream may become unavailable anytime.
---
Method to solve the problem: 7x24 continuously tries to pull the state of the RTSP stream; if the stream is active, immediately reads through the stream and write to disk until the stream becomes unavailable again. 
---
Some requirements:
1. 7x24 pull and check the RTSP stream url to see if it's active. 
	a. If it's closed, do nothing and sleep 1 second.
	b. If it's active, start to read until the RTSP stream URL is closed.
		i. Be careful of handling the RTSP stream closed suddently that make sure no data loss. 
2. Save the video to mp4 format and keep original quality and resolution.
3. Support multiple cameras that we can define each camera's name and rstp url.
4. Handle exceptions to reduce resource leaking.
5. The script accepts the camera_name, its RTSP_URL, and the output_path as arguments
6. The script manages the output path as hierarchy: output_path/camera_name/year/month/day/
7. Only print to the STDOUT if video successfully read and written. The format of print: Name_file	File_size(in MB)
8. Prevent generated file gets corrupted after the RTSP stream closed suddently. 
9. Prevent generated empty files. 



---
sudo apt-get install supervisor  

sudo vi /etc/supervisor/conf.d/cam.conf

[program:cam]  
command=bash start.sh cam rtsp://user:pass@ip/live0 /output_path/
autostart=true  
autorestart=true  
startretries=3  
stderr_logfile=/var/log/rtsp/cam.err.log  
stdout_logfile=/var/log/rtsp/cam.out.log  
user=user 

sudo supervisorctl reread  
sudo supervisorctl update  

sudo supervisorctl start cam  





[program:backup]
environment=PATH="%(ENV_PATH)s:$Azcopy_Path",AZCOPY_JOB_PLAN_LOCATION="/var/log/rtsp/azcopy_job_plan.log",AZCOPY_LOG_LOCATION="/var/log/rtsp/azcopy_job.log"
command=bash $Code_repo_path/backup.sh "Data_path" "Storage_Account" "Container" "SAS"
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/rtsp/backup.err.log
stdout_logfile=/var/log/rtsp/backup.out.log
user=user




openssl enc -aes-256-cbc -d -in x.enc -out x.mp4 -k password -salt -md md5


---
# Openssl
## Download openssl 
wget https://www.openssl.org/source/old/1.1.0/openssl-1.1.0l.tar.gz

## Compile openssl
```
tar zxf openssl-1.1.0l.tar.gz 
cd openssl-1.1.0l/
./config no-asm shared no-async --prefix=/live555_path/openssl
make
make install
```

# Live555
## Download live555
wget http://www.live555.com/liveMedia/public/live.2023.07.24.tar.gz

## Configure live555
```
COMPILE_OPTS =          $(INCLUDES) -I/live555_path/openssl/include -I. -O2 -DSOCKLEN_T=socklen_t -D_LARGEFILE_SOURCE=1 -D_FILE_OFFSET_BITS=64 -DNO_STD_LIB
...
CPLUSPLUS_FLAGS =       $(COMPILE_OPTS) -Wall -DBSD=1 $(CPPFLAGS) $(CXXFLAGS) -std=c++11
...
LDFLAGS=                -L /live555_path/openssl/lib
...
```

# Compile live555
./genMakefiles linux
make -j4