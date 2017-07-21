'''
Reading GMAIL using Python
	- Kinshuk Chandra
'''

'''
Before running this script, the user should get the authentication by following 
the link: https://developers.google.com/gmail/api/quickstart/python
Also, client_secret.json should be saved in the same directory as this file
'''

import base64
import email.mime.text
import os
import sys

# Importing required libraries
from apiclient import discovery
from apiclient import errors
from bs4 import BeautifulSoup
from httplib2 import Http
from oauth2client import file, client, tools

import config as conf

sys.path.append("/Users/kchandra/Lyf/Kode/SCM/Github/k2/GmaiLCleaner/moonpie")
import moonpie
from moonpie.color_util import PrintInColor as pic

ALLOWED_SCOPES = ['https://mail.google.com/',
                  'https://www.googleapis.com/auth/gmail.compose',
                  'https://www.googleapis.com/auth/gmail.modify',
                  'https://www.googleapis.com/auth/gmail.send']
from lru import LRUCacheDict


class PythonGmailAPI:
    GMAIL = None
    user_id = 'me'

    def initialize(self, secretJson):
        # If modifying these scopes, delete your previously saved credentials by removing file storage.json.
        # Creating a storage.JSON file with authentication details
        SCOPES = 'https://mail.google.com/'  # we are using this to delete the emails

        store = file.Storage('storage.json')

        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(secretJson, SCOPES)
            creds = tools.run_flow(flow, store)
        self.GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

    def __init__(self, secretJson):
        self.initialize(secretJson)
        self.cache = LRUCacheDict(max_size=10000, expiration=24*60*60)#24 h cache

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
        print(unread_msgs)
        # We get a dictonary. Now reading values for the key 'messages'
        mssg_list = []
        if 'messages' in unread_msgs:
            mssg_list = unread_msgs['messages']
        print("Total unread messages in inbox: ", str(len(mssg_list)))
        return mssg_list

    '''
    Return list of label 
    Sample label: 
    {
		'id': 'Label_187',
		'name': 'some label names',
		'messageListVisibility': 'show',
		'labelListVisibility': 'labelShow',
		'type': 'user'
	}
    '''

    def get_all_labels(self, user_id='me'):
        all_labels = self.GMAIL.users().labels().list(userId=user_id).execute()
        return all_labels

    def get_message_data(self, m_id, user_id='me'):
        if m_id in self.cache:
            print("Got from cache")
            return self.cache[m_id]
        message = self.GMAIL.users().messages().get(userId=user_id, id=m_id).execute()  # fetch the message using API
        payload = message['payload']  # get payload of the message
        headr = payload['headers']  # get header of the payload

        mssg_dic = {}
        mssg_dic['labelIds'] = message['labelIds']

        for one in headr:  # getting the Subject
            if one['name'] == 'Subject':
                msg_subject = one['value']
                mssg_dic['subject'] = msg_subject
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
                mssg_dic['from'] = msg_from
                mssg_dic['fromName'] = msg_from.split(" <")[0]
                if " <" in msg_from:
                    mssg_dic['fromEmail'] = msg_from.split(" <")[1].replace(">", "")
                else:
                    mssg_dic['fromEmail'] = msg_from.split(" <")[0]
            else:
                pass

        mssg_dic['snippet'] = message['snippet']  # fetching message snippet
        part_data = ""
        try:
            # If the message is large, it comes in parts
            if 'parts' in payload:
                # Fetching message body
                mssg_parts = payload['parts']  # fetching the message parts
                for i in (0, len(mssg_parts) - 1):
                    part_i = mssg_parts[i]  # fetching first element of the part
                    part_data_i = moonpie.get_multi_level_val_from_dict(part_i, "body/data")
                    if part_data_i is not None:
                        # NOTE: I am adding body part earliest body part first
                        part_data = str(part_data_i) + part_data

            # If the message is small, it is directly available
            elif 'body' in payload:
                part_data = moonpie.get_multi_level_val_from_dict(payload, "body/data")
            else:
                print(message)
            mssg_body = ""
            if part_data is not None:
                mssg_body = PythonGmailAPI.get_data_from_base64(part_data, mssg_dic)
                if mssg_body is None or '':
                    print(message)
            # mssg_body is a readible form of message body
            # depending on the end user's requirements, it can be further cleaned
            # using regex, beautiful soup, or any other method
            mssg_dic['body'] = mssg_body

        except Exception as e:
            pic.red(e)
            pic.red(message)
            pass
        self.cache[m_id] = mssg_dic
        return mssg_dic

    @staticmethod
    def get_data_from_base64(b64_data, temp_dict):
        clean_one = b64_data.replace("-", "+")  # decoding from Base64 to UTF-8
        clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
        clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
        mssg_body = ''
        try:
            soup = BeautifulSoup(clean_two, "lxml")
            mssg_body = str(soup.body())
        except Exception as e:
            pic.red("Not a valid html or xml, so moving back to raw text.More: {}".format(e))
        if mssg_body is None:
            mssg_body = clean_two
        return mssg_body

    @staticmethod
    def get_message_id_list_from_raw_messages(raw_messages):
        message_list = []
        message_list.extend([str(d['id']) for d in raw_messages])
        print("got {0} ids".format(len(message_list)))
        return message_list

    # WARNING - This will actually delete the message forever
    def batch_delete_messages_given_raw_messages(self, mssg_list, user_id='me'):
        messages_list = PythonGmailAPI.get_message_id_list_from_raw_messages(mssg_list)
        message = {
            'ids': messages_list
        }
        self.batch_delete_messages(message, user_id=user_id)

    # WARNING - This will actually delete the message forever
    '''
        messages: {ids: [m_id1, m_id2...] }
    '''

    def batch_delete_messages(self, messages, user_id='me'):
        print("ready to delete {} messages".format(len(messages['ids'])))

        self.GMAIL.users().messages().batchDelete(
            userId=user_id,
            body=messages
        ).execute()

        print("I deleted stuff!")

    '''
    message_list = list of message ids, addLabelIds=list of labels to be added, 
    removeLabelIds = list of labels to be removed from all the messages
    '''

    def batch_modify_messages(self, message_list, addLabelIds, removeLabelIds=[], user_id='me'):
        print("ready to modify {} messages".format(len(message_list)))
        if len(message_list) == 0:
            print("No message to modify")
            return
        # CREATE a message body
        label_body = {
            "ids": message_list,
            "removeLabelIds": removeLabelIds,
            "addLabelIds": addLabelIds,
        }
        self.GMAIL.users().messages().batchModify(
            userId=user_id,
            body=label_body
        ).execute()

        print("I trashed stuff!")

    def batch_trash_mail_given_raw_messages(self, mssg_lst, user_id='me'):
        """ Move a Mail to Trash"""
        try:
            messages_list = PythonGmailAPI.get_message_id_list_from_raw_messages(mssg_lst)
            self.batch_modify_messages(messages_list, user_id=user_id, addLabelIds=['TRASH'])
        except errors.HttpError as error:
            pic.red('An error occurred: {}'.format(error))

    def show_unread_email(self):
        """
        Fetch Unread emails from gmail and show them here.
        """
        service = self.GMAIL
        try:
            results = service.users().messages().list(userId='me').execute()
        except errors.HttpError as e:
            print('An error occurred: {}' % e)

        messages = results.get('messages', [])

        for message in messages:
            message_id = message['id']
            try:
                msg_data = service.users().messages().get(userId='me', id=message_id).execute()
                self.mark_as_read(message_id)
            except errors.HttpError as e:
                print('An error occurred: {}' % e)

            payload = msg_data['payload']
            labels = msg_data['labelIds']
            attached_file = payload['filename']
            body = payload['body']
            headers = payload['headers']
            snippet = msg_data['snippet']

            print("--------------------------------------------------")
            print("Message ID : " + message_id)
            options = [
                'To',
                'From',
                'Subject',
                'Date',
                'List-unsubscribe'
            ]
            unsubscribe_url = ""
            for item in headers:
                if item['name'] in options:
                    print(item['name'] + " : " + item['value'])
            print(",  ".join(labels))
            print("Mail Snippet : " + snippet)
            if attached_file != '':
                print("Attached File : " + attached_file)
                print("Attached File : " + attached_file)
                # DownloadAttachment(attachmentId)
                # break

    def mark_as_read(self, m_id, user_id='me'):
        self.GMAIL.users().messages().modify(userId=user_id, id=m_id, body={'removeLabelIds': ['UNREAD']}).execute()

    # WARNING - This will actually delete the message forever
    def delete_message(self, messageId, user_id='me'):
        """ Delete a message permanently"""

        try:
            results = self.GMAIL.users().messages().delete(userId=user_id, id=messageId).execute()
            print("Message Deleted ..")
        except errors.HttpError as error:
            print('An error occurred: {}' % error)
        print(results)

    def trash_mail(self, messageId, user_id='me'):
        """ Move a Mail to Trash"""
        try:
            results = self.GMAIL.users().messages().trash(userId=user_id, id=messageId).execute()
            print("Mailed moved to trash..")
        except errors.HttpError as error:
            print('An error occurred: {}'.format(error))

    def untrash_mail(self, messageId, user_id='me'):
        """ Move a Mail to Trash"""
        try:
            results = self.GMAIL.users().messages().untrash(userId=user_id, id=messageId).execute()
            print("Mailed moved to trash..")
        except errors.HttpError as error:
            print('An error occurred: {}'.format(error))

    def save_to_drafts(self, user_id='me', message=""):

        try:
            message = (self.GMAIL.users().drafts().create(userId=user_id, body=message).execute())
            print('Message Id: {}'.format(message['id']))
            return message
        except errors.HttpError as error:
            print('An error occurred: {}'.format(error))


def main():
    # sender_address = input('Sender address: ')
    # to_address = input('To address: ')
    # subject = input('Subject: ')
    # body = input('Body: ')
    # PythonGmailAPI().gmail_send(sender_address, to_address, subject, body)
    gmail = PythonGmailAPI(conf.GMAIL_CLIENT_SECRET_FILE)
    labels = gmail.get_all_labels()
    print(labels)


if __name__ == '__main__':
    main()
