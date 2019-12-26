from __future__ import print_function
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
from apiclient import errors
from apiclient import http
import logging

from apiclient import discovery

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


# To list folders
def listfolders(service, filid, des):
    results = service.files().list(
        pageSize=1000, q="\'" + filid + "\'" + " in parents",
        fields="nextPageToken, files(id, name, mimeType)").execute()
    # logging.debug(folder)
    folder = results.get('files', [])
    for item in folder:
        if str(item['mimeType']) == str('application/vnd.google-apps.folder'):
            if not os.path.isdir(des+"/"+item['name']):
                os.mkdir(path=des+"/"+item['name'])
            print(item['name'])
            listfolders(service, item['id'], des+"/"+item['name'])  # LOOP un-till the files are found
        else:
            downloadfiles(service, item['id'], item['name'], des)
            print(item['name'])
    return folder


# To Download Files
def downloadfiles(service, dowid, name,dfilespath):
    request = service.files().get_media(fileId=dowid)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(dfilespath + "\\" + name, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())


if __name__ == '__main__':
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

    service = build('drive', 'v3', credentials=creds)

    with open("download_links.txt", "r") as fh:
        lines = fh.readlines()

    for i in range(len(lines)):
        folder_id = lines[i].strip().split("id=")[-1]
        results = service.files().list(
            pageSize=1000, q="'{}' in parents".format(folder_id), fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(item)
                try:
                    if not os.path.isdir("train\\"+folder_id):
                        os.mkdir("train\\"+folder_id)
                    filepath = os.getcwd() + "\\train\\"+folder_id
                    downloadfiles(service, item['id'], item['name'], filepath)
                except:
                    print("failed ", folder_id)