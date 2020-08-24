from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from datetime import date
import io
import os
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
            
    now = date.today()
    #print(now.strftime("%Y"))
    day = now.strftime("%d")
    month = now.strftime("%m")
    year = now.strftime("%Y")
    
    d1=(int(day))
    
    if d1 < 10:
        day='0'+str(d1-1)
        #print(day)
    
    dat = []
    dat.append(year)
    dat.append(month)
    dat.append(day)
    print(dat)
    directory = "D:/Testwer/" + year + "/" + month + "/" + day + "/"
    folder = "wxarchive"
    file="00"
    
    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    queries = [
        "mimeType = 'application/vnd.google-apps.folder'",
        "sharedWithMe"
    ]
    
    drive_str_query = queries[0] if len(queries) == 1 else " and ".join(queries)
    results = service.files().list(q=drive_str_query,
                                   pageSize=1000,
                                   spaces='drive',
                                   fields="files(id, name)").execute()
    
    items = results.get('files', [])
   # print(items)
    
    id = ""
    for item in items:
        if folder == item['name']:
            id = item['id']
            break
    #print(id)    
    
    for d in dat:
        queries = [
        "mimeType = 'application/vnd.google-apps.folder'",
        "'" + id +"'" + " in parents"
        ]
        drive_str_query = queries[0] if len(queries) == 1 else " and ".join(queries)
        results = service.files().list(q=drive_str_query,
                                   pageSize=1000,
                                   spaces='drive',
                                   fields="files(id, name)").execute()
                            
        items = results.get('files', [])

        for item in items:
            if d == item['name']:
                id = item['id']
                break
             
                    
    queries = [
        "mimeType = 'application/vnd.google-apps.folder'",
        "'" + id +"'" + " in parents"
    ]
    
    #print(queries);
    drive_str_query = queries[0] if len(queries) == 1 else " and ".join(queries)
    results = service.files().list(q=drive_str_query,
                                   pageSize=1000,
                                   spaces='drive',
                                   fields="files(id, name)").execute()
    #print("2nd col")
    items = results.get('files', [])
    
    #print(items)    
    global dayStr
    #dayStr = "12"
    #print(dayStr)
    #print(dat[2])
    #for item in items:
     #   if dat[2] == item['name']:
      #      id = item['id']
       #     print(id)
        #    dayStr = item['name']
         #   print(dayStr)
          #  break
        
    directory = directory #+ dayStr + "/"
    
    results = service.files().list(q="'" + item['id'] +"'" + " in parents",
                                   pageSize=1000,
                                   spaces='drive',
                                   fields="files(id, name)").execute()
    fileItems = results.get('files', [])
    print(fileItems)

    for fileItem in fileItems:
        file_id = str(fileItem['id'])
        fileFolder_name = fileItem['name']
        downloadDir = directory + fileFolder_name + "/"
        fileResults = service.files().list(q="'" + fileItem['id'] +"'" + " in parents",
                                pageSize=1000,
                                spaces='drive',
                                fields="files(id, name)").execute()
        finalFileItems = fileResults.get('files', [])
        #print(downloadDir)
        os.makedirs(downloadDir)
        for finalFileItem in finalFileItems:
            finalFile_id = str(finalFileItem['id'])
            request = service.files().get_media(fileId=finalFile_id)
            file_io_base = open(downloadDir + finalFileItem['name'],'wb')
            #fh = io.BytesIO()
            downloader = MediaIoBaseDownload(file_io_base, request)
            #print(fh)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                #print(status)
                print ("Download %d%%." % int(status.progress() * 100))


if __name__ == '__main__':
    main()