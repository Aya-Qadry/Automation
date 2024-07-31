import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import threading
import time

import webbrowser
from webbrowser import register

import base64

# readonly acess => read messages and threads , access labels , search emails and metadata (such as headers)
# it does not allow sending emails or modifying or deleting any email
#SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


# routes are just there to organize the process logically => crucial aspect is the content of these functions - what they do

def get_gmail_service() : 
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists('token.pickle') : 
        with open('token.pickle' , 'rb') as token : 

            # pickle is used for serializing and deserializing Python objects
            creds = pickle.load(token)
            # the credentials are loaded

    if not creds or not creds.valid : 
        if creds and creds.expired and creds.refresh_token : 
            creds.refresh(Request())
        else : 

            brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            register('brave' , None , webbrowser.BackgroundBrowser(brave_path))

            credentials_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path , SCOPES
            )
            creds = flow.run_local_server(port=0 , browser='brave')

        #Save the credentials
        with open('token.pickle' , 'wb') as token : 
            pickle.dump(creds,token)

    service = build('gmail' , 'v1' , credentials=creds)

#    session['state'] = state 
    
    return service

def get_email_content(msg) : 
    try : 
        #payload is the main content of the email message
        payload = msg['payload']
        if 'parts' in payload : 
            for part in payload['parts'] : 
                if part['mimeType'] == 'text/plain' : 
                    body_data = part['body']['data']
                    decoded_data = base64.urlsafe_b64decode(body_data).decode('utf-8')
                    return decoded_data
                elif 'body' in payload : 
                    body_data = payload['body']['data']
                    decoded_data = base64.urlsafe_b64decode(body_data).decode('utf-8')
                    return decoded_data
    except Exception as e:
        print(f"Error extracting email body : {e}")
    
    return None

from nlp_extraction import retreive_data

def watch_emails() : 

    service = get_gmail_service()

    #id of the message , so that its not processed twice : 
    processed_ids = set()

    while True : 
        try : 
            results = service.users().messages().list(userId='me' , labelIds=['INBOX'],
                                                      q = "subject: DEPOT DE MARQUE is:unread").execute()
            
            messages = results.get('messages' , [])

            #for message in messages : 
            #process one message at a time : 
            if messages : 
                message = messages[0] # first obvi
                message_id = message['id']
                print(f"message id : {message_id}")
                if message_id not in processed_ids : 
                    msg = service.users().messages().get(userId='me' , id=message_id).execute()
                    main_content = get_email_content(msg)
                
                    # processus d'extraction de marque
                    retreive_data(main_content)
                    
                    #mark as read : 
                    service.users().messages().modify(userId='me' , id=message['id'], body={'removeLabelIds' : ['UNREAD']}).execute()
                    
                    processed_ids.add(message_id)
                break

            time.sleep(10)
            

        except Exception as e:
            print(f"An error occurred: {type(e).__name__}: {str(e)}")
            if hasattr(e, 'resp'):
                print(f"Response status: {e.resp.status}")
                print(f"Response content: {e.content}")
            time.sleep(10)

def setup_email_watcher() : 
    email_thread = threading.Thread(target=watch_emails)
    email_thread.daemon = True
    email_thread.start()     


