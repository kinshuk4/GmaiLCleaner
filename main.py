# Importing required libraries
# import dateutil.parser as parser

import config as conf
from gmailclient import PythonGmailAPI
from pocketclient.pocket_client import PythonPocketAPI
from aridcaravan import GmailPocket

'''
This script does the following:
- Go to Gmail inbox
- Find and read all the unread messages
- Extract URLs and send it to pocket
- Delete the email 
'''

import sys

sys.path.append("/Users/kchandra/Lyf/Kode/SCM/Github/k2/GmaiLCleaner/moonpie")

print("Initializing the gmail api")
gmail = PythonGmailAPI(conf.GMAIL_CLIENT_SECRET_FILE)

print("Initializing the pocket api")
pocket = PythonPocketAPI(conf.POCKET_CLIENT_SECRET_FILE)

workflow1 = GmailPocket(gmail, pocket)
# workflow1.labelToPocket(conf.get_labels(), headersToExclude=conf.POCKET_SUBJECT_TO_EXCLUDE_LIST, emailIdToDomain=conf.EMAIL_ID_TO_DOMAIN_DIC)
workflow1.filterToPocket(conf.GOOGLE_FILTER_CFINANCIAL, headersToExclude=conf.POCKET_SUBJECT_TO_EXCLUDE_LIST, emailIdToDomain=conf.EMAIL_ID_TO_DOMAIN_DIC)
