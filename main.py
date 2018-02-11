""" Will take in vimwiki pages and write to goole docs """
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload

from FileManager import FileManager
from ConfigParser import ConfigParser

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# Read in the config file
config = ConfigParser()
config.read('dev.ini')

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = config.get('googleinfo', 'scope')
CLIENT_SECRET_FILE = config.get('googleinfo', 'secret_file')
APPLICATION_NAME = config.get('googleinfo', 'application_name')


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            if config.get('googleinfo', 'parent_folder') in item['name']:
                dir_id = item['id']
        
        print(dir_id)

    wiki_path = config.get('localinfo', 'wiki_path') 
    fm = FileManager(wiki_path)
    files = fm.get_files_after_date(config.get('localinfo', 'after_date'))

    for f in files:
        file_metadata = {
            'name': f,
            'parents': [dir_id]
        }
        f_path = os.path.join(wiki_path, f)
        print(f_path)
        media = MediaFileUpload(os.path.join(wiki_path, f), mimetype='text/plain')
        service.files().create(body=file_metadata,
            media_body=media,
            fields='id').execute()

if __name__ == '__main__':
    main()
