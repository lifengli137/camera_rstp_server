#!/bin/bash  
  
path="$1"
storage_account="$2"  
storage_container="$3"  
storage_sas_token="$4"  
azcopy_path="$5


# Traverse the folder and process files  
find $path -type f -print0 | while IFS= read -r -d $'\0' file; do  
    # Upload the file to Azure Blob Storage  

    relative_path=${file#$path}
    
    export PATH=$PATH:$azcopy_path
    azcopy cp "$file" "https://$storage_account.blob.core.windows.net/$storage_container/$relative_path?$storage_sas_token" --overwrite=false --put-md5 --check-md5 FailIfDifferent
    exit_code=$?
    # If the upload was successful, remove the local file  
    if [ $exit_code -eq 0 ]; then  
        #rm "$file"  
        echo "File $file uploaded and removed successfully."  
    else  
        echo "Error: File $file failed to upload. Exit code: $exit_code"  
    fi  
done  

# Remove empty directories  
#find $path -type d -empty -delete  
echo "find $path -type d -empty -delete"
  
