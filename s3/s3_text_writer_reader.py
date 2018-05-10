## this script is a basic utility for interacting w S3 to write text files for
## public read

import boto3
from botocore.client import Config
from boto3 import client


class s3_text_writer_reader():
    ''' this is a class which references your local aws creds to write files
    using boto to s3 buckets. can also be used to retrieve those files'''
    def __init__(self):
       ''' starts the authenticated s3 sessions'''
       session = boto3.Session()
       config = Config(signature_version='s3v4', connect_timeout=10)
       s3=session.resource('s3', use_ssl=True, config=config)
       self.loaded = s3

    def get_object(self,bucket,file_path):
       '''
       loads an object from a bucket with a file path
       example:
       bucket='postfiat1',file_path=1.txt'
       '''
       obj=self.loaded.Object(bucket,file_path)
       return obj

    def check_if_object_exists(self,bucket,file_path):
       ''' pass in a bucket and a file path and check if it exists.
       useful to do before running functions '''

       zz=self.loaded.Object(bucket,file_path)
       exists = False
       try:
           zz.load()
           exists=True
       except:
           pass
       return exists

    def load_object_contents_if_exists(self, bucket, file_path):
        ''' reads in an object from a file path

        '''
        file_exists=self.check_if_object_exists(bucket=bucket,
                                    file_path=file_path)
        if file_exists == False:
            print('file does not exist')
        if file_exists == True:
            obj=self.get_object(bucket=bucket,file_path=file_path)
            output=raw_data=obj.get()['Body'].read()
            return output


    def write_output_object(self,object_contents,bucket,file_path,public=True):
        obj= self.get_object(bucket=bucket,file_path=file_path)
        if public == True:
            obj.put(Body=object_contents, ACL='public-read')
        if public == False:
            obj.put(Body=object_contents)
