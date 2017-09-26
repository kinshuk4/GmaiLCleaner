import sys

sys.path.append("/Users/kchandra/Lyf/Kode/SCM/Github/k2/GmaiLCleaner/moonpie")
import moonpie

sys.path.append("/Users/kchandra/Lyf/Kode/SCM/Github/k2/GmaiLCleaner/gmailclient")
import gmailclient
from gmailclient.filter import Filter

sys.path.append("/Users/kchandra/Lyf/Kode/SCM/Github/k2/GmaiLCleaner/pocketclient")
import pocketclient

sys.path.append("/Users/kchandra/Lyf/Kode/SCM/Github/k2/GmaiLCleaner/aridcaravan")

import aridcaravan.gmail_cleaner_util as gcu
import uuid
from lru import LRUCacheDict


class GmailPocket:
    def __init__(self, gmailClient, pocketClient):
        self.gmail = gmailClient
        self.pocket = pocketClient
        self.cache = LRUCacheDict(max_size=10000, expiration=24 * 60 * 60)

    @staticmethod
    def writeMsgUrls(all_urls):
        unique_filename = "test/" + str(uuid.uuid4())
        thefile = open(unique_filename, 'w')

        for item in all_urls:
            thefile.write("%s\n" % item)

    @staticmethod
    def exclude_message_on_subject(HEADERS_TO_EXCLUDE, subject_string):
        if any(header.lower() in subject_string.lower() for header in HEADERS_TO_EXCLUDE):
            return True
        return False

    def getUrlsFromGmailMessage(self, message_dic, debug=False, headersToExclude=set(), emailIdToDomain={}):
        print(message_dic['subject'])
        if GmailPocket.exclude_message_on_subject(headersToExclude, message_dic['subject']):
            return
        if debug:
            print("++++++++++++++++++++++ MESSAGE DICTIONARY ++++++++++++++++++++++++++++")
            print(message_dic)
        message_body_without_footer = gcu.get_mailbody_without_footer(message_dic['body'])
        if debug:
            print("++++++++++++++++++++++ MESSAGE BODY WITHOUT FOOTER ++++++++++++++++++++++++++++")
            print(message_body_without_footer)
        urls = gcu.extract_urls_from_body(message_body_without_footer)
        urls = list(urls)
        for known_senders_without_urls in emailIdToDomain:
            if known_senders_without_urls in message_dic['from']:
                url_from_domain = gcu.get_url_for_sender_email_id(known_senders_without_urls)
                urls.extend(url_from_domain)

        print(urls)
        return urls

    def messageListToPocket(self, mssg_list, debug=False, headersToExclude=set(), emailIdToDomain={}, delete=False):
        final_list = []
        all_urls = set()
        all_ids = []
        moonpie.PrintInColor.green(
            "Total messaged retrieved in before url reading in messageToPocket: " + str(len(mssg_list)))
        message_dic = {}
        for mssg in mssg_list:
            m_id = mssg['id']  # get id of individual message
            all_ids.append(m_id)
            if m_id in self.cache:
                print("Got from gmail_pocket cache")
                message_dic = self.cache[m_id]
                if delete:
                    urls = message_dic['urls']
                else:
                    print("Got from cache but delete is false, so not processing as can process multiple time")
                    continue
            else:
                message_dic = self.gmail.get_message_data(m_id)
                urls = self.getUrlsFromGmailMessage(message_dic, debug=debug, headersToExclude=headersToExclude,
                                                    emailIdToDomain=emailIdToDomain)
                if not urls:
                    continue
                message_dic['urls'] = urls
                self.cache[m_id] = message_dic
            all_urls.update(urls)
            print("------------------------------")
            final_list.append(message_dic)  # This will create a dictonary item in the final list

            # This will mark the messagea as read
            self.gmail.mark_as_read(m_id)

        moonpie.PrintInColor.green("Total messaged retrieved in messageToPocket: " + str(len(final_list)))
        print("Doing the batch jobs")

        print("Total urls retrieved: {}".format(len(all_urls)))

        print("Fav'ing all the urls")
        self.pocket.favourite(all_urls, 'g2p')
        if delete:
            moonpie.PrintInColor.red("Trashing all the emails from gmail now, got : " + str(len(mssg_list)))
            self.gmail.batch_trash_mail_given_raw_messages(mssg_list)

    def labelToPocket(self, labelIds, debug=False, headersToExclude=set(), emailIdToDomain={}):
        mssg_list = []
        for gmail_labels_ids in labelIds:
            curr_mssg_list = self.gmail.get_messages_for_labels(labelIds=gmail_labels_ids)
            mssg_list.extend(curr_mssg_list)
        moonpie.PrintInColor.green("Total messaged retrieved from Label: " + str(len(mssg_list)))
        self.messageListToPocket(mssg_list, headersToExclude=headersToExclude, emailIdToDomain=emailIdToDomain,
                                 debug=debug)

    def filterToPocket(self, filterStr, debug=False, headersToExclude=set(), emailIdToDomain={}, delete=False):
        labelIds = [['INBOX'], ['SPAM']]  #
        mssg_list = []
        for gmail_labels_ids in labelIds:
            curr_mssg_list = self.gmail.get_messages_for_labels(labelIds=gmail_labels_ids)
            mssg_list.extend(curr_mssg_list)
        moonpie.PrintInColor.green("Total messaged retrieved from Manual Filtering: " + str(len(mssg_list)))
        f = Filter.fromFilterString(filterStr=filterStr)
        print(f)
        filtered_mssg_list = []
        all_urls = set()
        i = 0
        for mssg in mssg_list:
            m_id = mssg['id']
            message_dic = self.gmail.get_message_data(m_id)
            i = i + 1
            if i % 100 == 0:
                moonpie.PrintInColor.green("{} of {} messages are manually filtered".format(i, len(mssg_list)))
                moonpie.PrintInColor.green(
                    "Total messaged retrieved from Manual Filtering: " + str(len(filtered_mssg_list)))
                self.messageListToPocket(filtered_mssg_list, headersToExclude=headersToExclude,
                                         emailIdToDomain=emailIdToDomain,
                                         debug=debug, delete=delete)
                # reset the message list
                filtered_mssg_list = []
            if f.isMessageFiltered(message_dic):
                filtered_mssg_list.append(mssg)
                print("------------------------------")

        moonpie.PrintInColor.green("Total messaged retrieved from Manual Filtering: " + str(len(filtered_mssg_list)))
        self.messageListToPocket(filtered_mssg_list, headersToExclude=headersToExclude, emailIdToDomain=emailIdToDomain,
                                 debug=debug, delete=delete)


        # self.messageListToPocket(filtered_mssg_list, headersToExclude=headersToExclude, emailIdToDomain=emailIdToDomain)
