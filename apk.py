# import packages
from google.cloud import storage
import os

# set key credentials file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'AIzaSyBBkOtp5EJlNkGfEuIVPc6pCW0PSLLK1Dc'

# define function that list files in the bucket
def list_cs_files(bucket_name): 
    storage_client = storage.Client()

    file_list = storage_client.list_blobs(bucket_name)
    file_list = [file.name for file in file_list]

    return file_list

print(list_cs_files('test_demo_storage_bucket'))