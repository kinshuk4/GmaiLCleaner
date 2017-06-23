# Importing required libraries
# import dateutil.parser as parser
import uuid

import config as conf
from gmail_cleaner_util import extract_urls_from_body, get_mailbody_without_footer
from gmail_client import PythonGmailAPI
from pocket_client import PythonPocketAPI

'''
This script does the following:
- Go to Gmail inbox
- Find and read all the unread messages
- Extract URLs and send it to pocket
- Delete the email 
'''

DEBUG = False


def exclude_message_on_subject(subject_string):
    if any(header.lower() in subject_string.lower() for header in conf.HEADERS_TO_EXCLUDE):
        return True
    return False


print("Initializing the gmail api")
gmail = PythonGmailAPI(conf.GMAIL_CLIENT_SECRET_FILE)

print("Initializing the pocket api")
pocket = PythonPocketAPI(conf.POCKET_CLIENT_SECRET_FILE)

gmail_labels = conf.get_labels()
mssg_list = []
for gmail_labels_ids in gmail_labels:
    curr_mssg_list = gmail.get_messages_for_labels(labelIds=gmail_labels_ids)
    mssg_list.extend(curr_mssg_list)

final_list = []
all_urls = set()
all_ids = []
for mssg in mssg_list:
    message_dic = {}
    m_id = mssg['id']  # get id of individual message
    all_ids.append(m_id)

    message_dic = gmail.get_message_data(m_id)
    if exclude_message_on_subject(message_dic['subject']):
        continue
    if DEBUG:
        print("++++++++++++++++++++++ MESSAGE DICTIONARY ++++++++++++++++++++++++++++")
        print(message_dic)
    message_body_without_footer = get_mailbody_without_footer(message_dic['body'])
    if DEBUG:
        print("++++++++++++++++++++++ MESSAGE BODY WITHOUT FOOTER ++++++++++++++++++++++++++++")
        print(message_body_without_footer)
    urls = extract_urls_from_body(message_body_without_footer)
    print(message_dic['subject'])
    print(urls)
    all_urls.update(urls)
    print("------------------------------")
    final_list.append(message_dic)  # This will create a dictonary item in the final list

    # This will mark the messagea as read
    gmail.mark_as_read(m_id)

print("Total messaged retrived: ", str(len(final_list)))
print("Doing the batch jobs")

print(len(all_urls))
unique_filename = "test/" + str(uuid.uuid4())
thefile = open(unique_filename, 'w')

for item in all_urls:
    thefile.write("%s\n" % item)

print("Fav'ing all the urls")
pocket.favourite(all_urls, 'g2p')

print("Trashing all the emails from gmail now")
gmail.batch_trash_mail_given_raw_messages(mssg_list)
