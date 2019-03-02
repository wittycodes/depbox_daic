BUCKET_NAME='daic-woz-data'


import json
import requests
import os 
from smart_open import smart_open
import boto3


s3=boto3.client('s3')

def cache_generate(session, download):
    


    print("-----------------------------------------------------------------------")
    print("file dumped into local cloud function storage from web.")
    print("now started uploading it into cloud stoage bucket's blob: ",download[1]) 
    r = session.get(download[0], stream = True)

    # -------------------------------------------------------
    key=download[1]
    with smart_open('s3://'+BUCKET_NAME+'/'+key, 'wb') as f:
        for chunk in r.iter_content(chunk_size=100*1024*1024): 
            if chunk:
                f.write(chunk)
    # -------------------------------------------------------
    
    print("uploaded into bucket: ",key)    
    





def daic_downloader():


    # ===================================================
    hostname='dcapswoz.ict.usc.edu'
    session = requests.Session()
    session.auth = ('daicwozuser','dA1c_U$3rW0zz')
    
    auth = session.post('http://' + hostname)
    hostname += '/wwwdaicwoz'
    response = session.get('http://' + hostname)
    htmlsrc = response.content
    # print(htmlsrc)
    # ===================================================
    


    # ==============================================================================
    from bs4 import BeautifulSoup as bs
    s=bs(htmlsrc,"html.parser")
    l=[]
    for link in s.find_all('a'):
        l.append(link.get('href'))

    links = [ [ 'http://' + hostname + '/' + x ,x] for x in l[5:]]
    for i in links:
        print(i);
    print("here, got all links in hand after scraping: apache_server indexof/")
    # ==============================================================================
    


    # ==============================================================================
    for download in links:

        b_data=s3.list_objects(Bucket=BUCKET_NAME)
        if "Contents" in b_data.keys():
            b_items=b_data["Contents"]
        else:
            b_items=[]
        hello = [ x['Key'] for x in b_items]
        print(hello)

        key=download[1]
        if not key in hello:
            cache_generate(session,download)

    # ==============================================================================










def load(init):

    # bucket init
    # ------------------------------------------------------------------
    daic_downloader()
    # ------------------------------------------------------------------


#   shell build commands
#   gcloud compute --project "daic-220306" ssh --zone "us-central1-a" "diac"
#   python /daic/main.py 


load("start")
print("process finished :)")

exit()