#!/bin/bash  
  
path="$1"
storage_account="$2"  
storage_container="$3"  
storage_sas_token="$4"  

if [ -f /tmp/find.tmp ]; then  
  rm /tmp/find.tmp  
fi  

while true; do  
  # Find all files in the directory structure and output the paths to /tmp/find.tmp  
  find "$path" -type f > /tmp/find.tmp  
  files=$(cat /tmp/find.tmp)

  for file in $files; do
    relative_path=${file#$path}
      
    # Perform the azcopy and check the result  
    azcopy cp "$file" "https://$storage_account.blob.core.windows.net/$storage_container/$relative_path?$storage_sas_token" \
     --overwrite=false --put-md5 --check-md5 FailIfDifferent --block-blob-tier Cool   
     
    # Check if azcopy copy was successful  
    if [ $? -eq 0 ]; then  
      # Remove the local file  
      #rm "$file"  
      echo "File $file uploaded and removed successfully."
    else  
      echo "Error: Failed to transfer $file to Azure Blob Storage"  
    fi  
  done
     
  # Sleep for 4 hours  
  sleep 4h  
done  