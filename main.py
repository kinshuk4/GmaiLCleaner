from pocket import Pocket, PocketException
# Importing required libraries
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import re
import time
# import dateutil.parser as parser
from datetime import datetime
import datetime
import csv
from gmail_client import PythonGmailAPI
from pocket_client import PythonPocketAPI
import config as conf
import re
import uuid

'''
This script does the following:
- Go to Gmail inbox
- Find and read all the unread messages
- Extract URLs and send it to pocket
- Delete the email 
'''


def extract_urls(message_data):
    # sender_set, header_set = getPocketSenders()
    urls = set()

    subject = message_data['subject']

    if 'Label_181' in message_data['labelIds']:
        if any(header.lower() in subject.lower() for header in conf.HEADERS_TO_EXCLUDE):
            return urls
        print(subject)
        body = message_data['body']
        str_body = str(body)
        searched_urls = re.findall(conf.URL_REGEX, str_body)
        for url in searched_urls:
            if not any(ignore_url in url.lower() for ignore_url in conf.IGNORE_URLS):
                urls.add(url)
            else:
                print(url)
                print("==========================================================")

    print("--------------------------------------------------------------------")
    return urls


def check_url(url):
    url_lower = url.lower()
    if url_lower.endswith(".csv") \
            | url_lower.endswith(".dat") \
            | url_lower.endswith(".zip") | url_lower.endswith(".lst") | (";" in url_lower):
        return False
    if url_lower is None:
        print(url_lower)
    without_http = url_lower.replace("http://", "")
    without_http = without_http.replace("https://", "")
    parts = without_http.split('/')
    if len(parts) < 2:
        return False
    return True


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
    temp_dict = {}
    m_id = mssg['id']  # get id of individual message
    all_ids.append(m_id)
    temp_dict = gmail.get_message_data(m_id)
    urls = extract_urls(temp_dict)
    all_urls.update(urls)
    final_list.append(temp_dict)  # This will create a dictonary item in the final list

    # This will mark the messagea as read
    gmail.mark_as_read(m_id)

print("Total messaged retrived: ", str(len(final_list)))
print("Doing the batch jobs")

all_urls2 = []
for url in all_urls:
    if check_url(url):
        all_urls2.append(url)

print(len(all_urls2))
unique_filename = "test/" + str(uuid.uuid4())
thefile = open(unique_filename, 'w')

for item in all_urls:
    thefile.write("%s\n" % item)

# print("Fav'ing all the urls")
# pocket.favourite(all_urls2, 'g2p')

# print("Deleting all the emails from gmail now")
# gmail.batch_delete_messages_given_read(mssg_list)
# GMAIL.users().messages().batchDelete(userId=user_id, body=all_ids)
