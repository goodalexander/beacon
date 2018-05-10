from interactive_brokers import ib_account_summary
from s3 import s3_text_writer_reader
from encryption import basic_text_encryption
import pandas as pd
from wayback_machine import wayback_cache
import datetime
import os
import requests
import time
import json

class basic_account_summary_cache():
    def __init__(self):
        f=open(os.path.expanduser('~/.beacon_creds/creds'),'r')
        temp=f.read()
        f.close()
        self.beacon_manager_id=temp.split('beacon_manager_id=')[1].split('\n')[0]
        self.s3_client=s3_text_writer_reader.s3_text_writer_reader()
        self.encryption_client= basic_text_encryption.beacon_fernet_encrypt()
        self.s3_bucket_addr='https://s3.amazonaws.com/postfiat1/'

    def cache_manager_track_record(self):
        # this hits interactive brokers account to make summary
        tdf_json=ib_account_summary.output_summary_json()
        # encrypts text
        encrypted_text_for_s3=self.encryption_client.encrypt_text(tdf_json)
        # writes to s3 public read
        self.s3_client.write_output_object(object_contents=encrypted_text_for_s3,
                                           bucket='postfiat1',
                                      file_path=beacon_manager_id+'.txt',public=True)
        # saves result to wayback machine
        wayback_cache.save_url(url_to_cache=self.s3_bucket_addr+self.beacon_manager_id+'.txt')

    def load_manager_track_record(self):
        today=(datetime.datetime.today()+datetime.timedelta(1)).strftime('%Y%m%d')
        url_to_load=self.s3_bucket_addr+self.beacon_manager_id+'.txt'
        all_days_of_track_record= wayback_cache.ret_wayback_dataframe(cached_url=url_to_load,
                                            start_date='20180508', end_date=today, freq='D')

        def throttled_request_text(xurl,sleeptime):
            temp=requests.get(xurl)
            time.sleep(sleeptime)
            return temp.text
        # loads in encrypted track record and decrpyts
        t=all_days_of_track_record['full_archive_url'].apply(lambda x: throttled_request_text(x,1))
        all_days_of_track_record['encrypted_track_record']=t
        t1=all_days_of_track_record['encrypted_track_record'].apply(lambda x:self.encryption_client.decrypt_text(x))
        all_days_of_track_record['decrypted_track_record']=t1

        # reformats it into easy to understand flat dataframe
        all_index_parts=list(all_days_of_track_record.index)
        arr=[]
        for ind_num in all_index_parts:
            track_record_meta=all_days_of_track_record.loc[ind_num]
            json_track_record=json.loads(track_record_meta['decrypted_track_record'])
            temp_df=pd.DataFrame(json_track_record)
            temp_df['load_date']=track_record_meta['date']
            temp_df['full_archive_url']=track_record_meta['full_archive_url']
            arr.append(temp_df)
        output=pd.concat(arr)
        return output
