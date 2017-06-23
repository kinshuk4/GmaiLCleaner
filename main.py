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
import os
import url_util as uu

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


def extract_urls_from_body(body):
    # sender_set, header_set = getPocketSenders()
    urls = set()

    # print(subject)
    str_body = str(body)
    searched_urls = re.findall(conf.URL_REGEX, str_body)
    for url in searched_urls:
        if not any(ignore_url in url.lower() for ignore_url in conf.IGNORE_URLS):
            urls.add(url)
        else:
            pass
            # print(url)

    # cleanup URLs
    cleanedup_urls = set()
    if DEBUG:
        print("+++++++++++++++++++++++++ Got URL Set 1 +++++++++++++++++++++++++++")
    for url in urls:
        url_lower = url.lower()
        if DEBUG:
            print(url_lower)

        for x in conf.characters_exclusion:
            if x in url_lower:
                url_lower = url_lower.replace(x, "")
                cleanedup_urls.add(url_lower)
            else:
                cleanedup_urls.add(url_lower)

    # starting second set of rules
    all_urls_valid_for_pocket = []
    if DEBUG:
        print("+++++++++++++++++++++++++ Got URL Set 2 +++++++++++++++++++++++++++")
    for url in cleanedup_urls:
        # url needs encoding
        if DEBUG:
            print(url)
        if ';' in url:
            url = uu.decode_url(url)
            # TODO for some reason decoding is not working and not replacing &amp; to &
            url = url.replace('&amp;', '&')
        if check_url(url):
            all_urls_valid_for_pocket.append(url)
    return all_urls_valid_for_pocket


def check_url(url):
    url_lower = url.lower()
    url_without_query_param = uu.remove_query_params(url_lower)
    extension = os.path.splitext(url_without_query_param)[1]

    if extension in conf.extensions_to_exclude:
        return False

    # if any(x in url_lower for x in conf.characters_exclusion):
    #     return False
    if url_lower is None:
        print(url_lower)
    if uu.check_if_only_domain_name(url_lower):
        return False
    return True


def get_mailbody_without_footer(mail_body):
    mail_body_str = str(mail_body)
    for x in conf.footer_finder_strings:
        if x in mail_body_str:
            mail_without_footer = mail_body_str.split(x)[0]
            return mail_without_footer
    return mail_body_str


def get_mailbody_without_footer_careful(mail_body):
    mail_body_str = str(mail_body)
    body_length = len(mail_body_str)
    for x in conf.careful_footer_strings:
        if x in mail_body_str:
            location = mail_body_str.find(x)
            if location > 0.6 * body_length:
                mail_without_footer = mail_body_str.split(x)[0]
                return mail_without_footer

    return mail_body_str


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
