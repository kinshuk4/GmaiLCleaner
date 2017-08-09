# Importing required libraries
# import dateutil.parser as parser

import config as conf
from gmailclient import PythonGmailAPI
from pocketclient.pocket_client import PythonPocketAPI
from aridcaravan import GmailPocket
import time
import datetime
'''
This script does the following:
- Go to Gmail inbox
- Find and read all the unread messages
- Extract URLs and send it to pocket
- Delete the email 
'''

import sys


sys.path.append("/Users/kchandra/Lyf/Kode/SCM/Github/k2/GmaiLCleaner/moonpie")


def initApis():
    print("Initializing the gmail api")
    gmail = PythonGmailAPI(conf.GMAIL_CLIENT_SECRET_FILE)

    print("Initializing the pocket api")
    pocket = PythonPocketAPI(conf.POCKET_CLIENT_SECRET_FILE)
    return gmail, pocket

import traceback
def exception_to_string(excp):
   stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__)  # add limit=??
   pretty = traceback.format_list(stack)
   return ''.join(pretty) + '\n  {} {}'.format(excp.__class__,excp)

def main():
    gmail, pocket = initApis()
    date_of_exec = datetime.datetime.today().date()
    while True:
        try:
            if date_of_exec < datetime.datetime.today().date():
                gmail, pocket = initApis()
            workflow1 = GmailPocket(gmail, pocket)
            workflow1.labelToPocket(conf.get_labels(), headersToExclude=conf.POCKET_SUBJECT_TO_EXCLUDE_LIST,
                                    emailIdToDomain=conf.EMAIL_ID_TO_DOMAIN_DIC)
            workflow1.filterToPocket(conf.GOOGLE_FILTER_CFINANCIAL,
                                     headersToExclude=conf.POCKET_SUBJECT_TO_EXCLUDE_LIST,
                                     emailIdToDomain=conf.EMAIL_ID_TO_DOMAIN_DIC, debug=conf.DEBUG)
        except Exception as e:
            print("Error has occured while processing: {}".format(e))
            print(exception_to_string(e))
            pass
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        date_of_exec = datetime.datetime.today().date()
        print("Last run completed at: {}".format(st))
        time.sleep(120)




if __name__ == '__main__':
    main()
