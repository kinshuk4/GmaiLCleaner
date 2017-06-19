'''
Reading GMAIL using Python
	- Kinshuk Chandra
'''

'''
Before running this script, the user should get the authentication by following 
the link: https://developers.google.com/gmail/api/quickstart/python
Also, client_secret.json should be saved in the same directory as this file
'''

# Importing required libraries
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import datetime
import csv
import email.mime.text


class PythonGmailAPI:
    _GMAIL = None
    user_id = 'me'

    @property
    def GMAIL(self):
        return self._GMAIL

    @GMAIL.setter
    def GMAIL(self, secretJson):
        # If modifying these scopes, delete your previously saved credentials by removing file storage.json.
        # Creating a storage.JSON file with authentication details
        SCOPES = 'https://mail.google.com/'  # we are using this to delete the emails
        # SCOPES = ['https://mail.google.com/',
        #           'https://www.googleapis.com/auth/gmail.compose',
        #           'https://www.googleapis.com/auth/gmail.modify',
        #           'https://www.googleapis.com/auth/gmail.send']
        store = file.Storage('storage.json')

        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(secretJson, SCOPES)
            creds = tools.run_flow(flow, store)
        self.GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

    def __init__(self):
        pass

    def gmail_send(self, sender_address, to_address, subject, body):
        print('Sending message, please wait...')
        message = self.__create_message(sender_address, to_address, subject, body)
        credentials = self.__get_credentials()
        service = self.__build_service(credentials)
        raw = message['raw']
        raw_decoded = raw.decode("utf-8")
        message = {'raw': raw_decoded}
        message_id = self.__send_message(service, 'me', message)
        print('Message sent. Message ID: ' + message_id)

    def __get_credentials(self):
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
        credential_path = os.path.join(credential_dir, CREDENTIAL_FILE)
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + credential_path)
        return credentials

    def __create_message(self, sender, to, subject, message_text):
        """Create a message for an email.
        Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.
        Returns:
          An object containing a base64url encoded email object.
        """
        message = email.mime.text.MIMEText(message_text, 'plain', 'utf-8')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        encoded_message = {'raw': base64.urlsafe_b64encode(message.as_bytes())}
        return encoded_message

    ''' SECTION NOT WORKING YET
    def __create_message_with_attachment(self, sender, to, subject, message_text, file):
      message = email.mime.multipart.MIMEMultipart()
      message['to'] = to
      message['from'] = sender
      message['subject'] = subject
      msg = email.mime.text.MIMEText(message_text)
      message.attach(msg)
      content_type, encoding = mimetypes.guess_type(file)
      if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
      main_type, sub_type = content_type.split('/', 1)
      if main_type == 'text':
        fp = open(file, 'rb')
        msg = email.mime.text.MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
      elif main_type == 'image':
        fp = open(file, 'rb')
        msg = email.mime.image.MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
      elif main_type == 'audio':
        fp = open(file, 'rb')
        msg = email.mime.audio.MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
      else:
        fp = open(file, 'rb')
        msg = email.mime.base.MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
      filename = os.path.basename(file)
      msg.add_header('Content-Disposition', 'attachment', filename=filename)
      message.attach(msg)
      return {'raw': base64.urlsafe_b64encode(message.as_string())}
    '''

    def __send_message(self, service, user_id, message):
        """Send an email message.
        Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          message: Message to be sent.
        Returns:
          Sent Message ID.
        """
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        return message['id']

    def __build_service(self, secretJson='client_secret.json'):
        """Build a Gmail service object.
        Args:
            credentials: OAuth 2.0 credentials.
        Returns:
            Gmail service object.
        """
        if self.GMAIL is None:
            # If modifying these scopes, delete your previously saved credentials by removing file storage.json.
            # Creating a storage.JSON file with authentication details
            SCOPES = 'https://mail.google.com/'  # we are using this to delete the emails
            # SCOPES = ['https://mail.google.com/',
            #           'https://www.googleapis.com/auth/gmail.compose',
            #           'https://www.googleapis.com/auth/gmail.modify',
            #           'https://www.googleapis.com/auth/gmail.send']
            store = file.Storage('storage.json')

            creds = store.get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets(secretJson, SCOPES)
                creds = tools.run_flow(flow, store)
            GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

            user_id = 'me'
        return GMAIL

    def get_messages_for_labels(self, user_id='me', labelIds=[]):
        # Getting all the unread messages from Inbox
        # labelIds can be changed accordingly
        unread_msgs = self.GMAIL.users().messages().list(userId=user_id, labelIds=labelIds).execute()
        # We get a dictonary. Now reading values for the key 'messages'
        mssg_list = unread_msgs['messages']
        print("Total unread messages in inbox: ", str(len(mssg_list)))
        return mssg_list

    def get_all_labels(self, user_id='me'):
        all_labels = self.GMAIL.users().labels().list(userId=user_id).execute()
        return all_labels

    def get_message_data(m_id, user_id='me'):
        message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute()  # fetch the message using API
        payload = message['payload']  # get payload of the message
        headr = payload['headers']  # get header of the payload

        temp_dict = {}
        temp_dict['labelIds'] = message['labelIds']

        for one in headr:  # getting the Subject
            if one['name'] == 'Subject':
                msg_subject = one['value']
                temp_dict['subject'] = msg_subject
            else:
                pass

        for two in headr:  # getting the date
            if two['name'] == 'Date':
                # msg_date = two['value']
                # date_parse = (parser.parse(msg_date))
                # m_date = (date_parse.date())
                # temp_dict['Date'] = str(m_date)
                temp_str = 'hell'
            else:
                pass

        for three in headr:  # getting the Sender
            if three['name'] == 'From':
                msg_from = three['value']
                temp_dict['sender'] = msg_from
            else:
                pass

        temp_dict['snippet'] = message['snippet']  # fetching message snippet

        try:
            if 'parts' in payload:
                # Fetching message body
                mssg_parts = payload['parts']  # fetching the message parts
                part_one = mssg_parts[0]  # fetching first element of the part
                part_body = part_one['body']  # fetching body of the message
                part_data = part_body['data']  # fetching data from the body
            elif 'body' in payload:
                part_data = payload['body']['data']
            else:
                print(message)

            mssg_body = PythonGmailAPI.get_data_from_base64(part_data, temp_dict)
            # mssg_body is a readible form of message body
            # depending on the end user's requirements, it can be further cleaned
            # using regex, beautiful soup, or any other method
            temp_dict['body'] = mssg_body

        except Exception as e:
            print(e)
            pass

        return temp_dict

    @staticmethod
    def get_data_from_base64(b64_data, temp_dict):
        clean_one = b64_data.replace("-", "+")  # decoding from Base64 to UTF-8
        clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
        clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
        mssg_body = ''
        try:
            soup = BeautifulSoup(clean_two, "lxml")
            mssg_body = soup.body()
        except Exception as e:
            print(e)
        if mssg_body is None:
            print("Cannot read html")
            mssg_body = clean_two
        return mssg_body


def main():
    sender_address = input('Sender address: ')
    to_address = input('To address: ')
    subject = input('Subject: ')
    body = input('Body: ')
    PythonGmailAPI().gmail_send(sender_address, to_address, subject, body)


if __name__ == '__main__':
    main()
