

import os 
import tempfile as tmp
rootpath=os.getcwd()
print("ping ",rootpath)

import json
import requests
import os 
import extract_from_zip as extract


BUCKET_NAME='daic-woz-data'
out_dir=os.path.abspath(__file__+'/../extracted_data/')
zip_dir=os.path.abspath(__file__+'/../zips/')

def EXTRACT_IT_FROM_ZIP(file,f_name):
    if f_name.endswith('.zip'):
        extract.extract_files(file,out_dir,True)

def cache_generate(session, download, file):
    


    print("-----------------------------------------------------------------------")
    print("file dumped into local cloud function storage from web.")
    print("now started uploading it into cloud stoage bucket's blob: ",download[1]) 
    r = session.get(download[0], stream = True)

    # -------------------------------------------------------
    
    with open(file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    # -------------------------------------------------------
    
    print("uploaded into bucket: ",file)    
    





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
        print(i)
    print("here, got all links in hand after scraping: apache_server indexof/")
    # ==============================================================================
    



    # ---------------------------------------------------------------
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.exists(zip_dir):
        os.makedirs(zip_dir)
    # ---------------------------------------------------------------



    # ==============================================================================
     efor download in links[40:60]:
        f_name=download[1]
        file = os.path.join(zip_dir,f_name)
        
        cache_generate(session,download,file)
        EXTRACT_IT_FROM_ZIP(file,f_name)
                        
    
        
        print("removed file local storage")
        print("-----------------------------------------------------------------------")

    # ==============================================================================










def load(init):
    daic_downloader()


load("start")
print("process finished :)")

exit()