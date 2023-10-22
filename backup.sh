#!/bin/bash  
  
path="$1"
storage_account="$2"  
storage_container="$3"  
storage_sas_token="$4"  


# Traverse the folder and process files  
find $path -type f -print0 | while IFS= read -r -d $'\0' file; do  
    # Upload the file to Azure Blob Storage  

    #azcopy copy --overwrite=false --check-md5 "$file" "https://homeblob137.blob.core.windows.net/enc/${file#$path/}?sp=racwl&st=2023-10-22T22:44:49Z&se=2033-11-02T06:44:49Z&spr=https&sv=2022-11-02&sr=c&sig=I3AJpolboK5EukKb1W5jvdnshArug%2BUr63yPeWRr92c%3D"
    #exit_code=$?  
    echo "$file" 
    echo "https://$storage_account.blob.core.windows.net/$storage_container/${file#$path/}$storage_sas_token"
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
  
