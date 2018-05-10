import pandas as pd
import datetime
import time
import requests

def save_url(url_to_cache):
    ''' takes a sample URL and '''
    url_to_cache= url_to_cache.split('://')[-1:][0]
    url_to_req=f'http://web.archive.org/save/{url_to_cache}'
    requests.get(url_to_req)

def url_hist_on_timestamp_req_string(cached_url, date_stamp):
    ''' formats the request string for the wayback machine '''
    cached_url= cached_url.split('://')[-1:][0]
    return f'http://archive.org/wayback/available?url={cached_url}&timestamp={date_stamp}'

def req_wayback_date_content(cached_url, datestamp):
    zz=url_hist_on_timestamp_req_string(cached_url=cached_url,
                                   date_stamp=datestamp)
    hist_request=requests.get(zz)
    return hist_request.json()

def ret_wayback_dataframe(cached_url,start_date,end_date,freq='D'):

    '''returns a dataframe with archive urls from the wayback machine
    cached_url is what you want to look at, start_date
    '''
    date_series=pd.date_range(start=start_date, end=end_date, freq='D')
    date_strings_to_iterate=[i.strftime('%Y%m%d') for i in date_series]
    arr=[]
    for xdate in date_strings_to_iterate:
        temp=req_wayback_date_content(cached_url=cached_url,
                                 datestamp=xdate)
        arr.append(temp)
        time.sleep(1)

    process_df=pd.DataFrame(arr)
    process_df['full_archive_url']=process_df['archived_snapshots'].apply(lambda x: x['closest']['url'])
    output=process_df.groupby('full_archive_url').last()[['timestamp']].reset_index()
    output['date']=output['timestamp'].apply(lambda x: datetime.datetime.strptime(x,'%Y%m%d'))
    return output
