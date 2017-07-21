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


class GmailPocket:
    def __init__(self, gmailClient, pocketClient):
        self.gmail = gmailClient
        self.pocket = pocketClient

    @staticmethod
    def exclude_message_on_subject(HEADERS_TO_EXCLUDE, subject_string):
        if any(header.lower() in subject_string.lower() for header in HEADERS_TO_EXCLUDE):
            return True
        return False

    def messageToPocket(self, message_dic, debug=False, headersToExclude=set(), emailIdToDomain={}):
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

    def messageListToPocket(self, mssg_list, debug=False, headersToExclude=set(), emailIdToDomain={}):
        final_list = []
        all_urls = set()
        all_ids = []
        message_dic = {}
        for mssg in mssg_list:
            m_id = mssg['id']  # get id of individual message
            all_ids.append(m_id)

            message_dic = self.gmail.get_message_data(m_id)
            urls = self.messageToPocket(message_dic, debug=debug, headersToExclude=headersToExclude,
                                        emailIdToDomain=emailIdToDomain)
            all_urls.update(urls)
            print("------------------------------")
            final_list.append(message_dic)  # This will create a dictonary item in the final list

            # This will mark the messagea as read
            self.gmail.mark_as_read(m_id)

        moonpie.PrintInColor.green("Total messaged retrived: " + str(len(final_list)))
        print("Doing the batch jobs")

        print(len(all_urls))
        # unique_filename = "test/" + str(uuid.uuid4())
        # thefile = open(unique_filename, 'w')

        # for item in all_urls:
        #     thefile.write("%s\n" % item)

        print("Fav'ing all the urls")
        # self.pocket.favourite(all_urls, 'g2p')

        print("Trashing all the emails from gmail now")
        # self.gmail.batch_trash_mail_given_raw_messages(mssg_list)

    def labelToPocket(self, labelIds, debug=False, headersToExclude=set(), emailIdToDomain={}):
        mssg_list = []
        for gmail_labels_ids in labelIds:
            curr_mssg_list = self.gmail.get_messages_for_labels(labelIds=gmail_labels_ids)
            mssg_list.extend(curr_mssg_list)

        self.messageListToPocket(mssg_list, headersToExclude=headersToExclude, emailIdToDomain=emailIdToDomain,
                                 debug=debug)

    def filterToPocket(self, filterStr, debug=False, headersToExclude=set(), emailIdToDomain={}):
        labelIds = [['INBOX'], ['SPAM']]  #
        mssg_list = []
        for gmail_labels_ids in labelIds:
            curr_mssg_list = self.gmail.get_messages_for_labels(labelIds=gmail_labels_ids)
            mssg_list.extend(curr_mssg_list)
        f = Filter.fromFilterString(filterStr=filterStr)
        print(f)
        filtered_mssg_list = []
        all_urls = set()
        for mssg in mssg_list:
            m_id = mssg['id']
            message_dic = self.gmail.get_message_data(m_id)

            if f.isMessageFiltered(message_dic):
                urls = self.messageToPocket(message_dic, debug=debug, headersToExclude=headersToExclude,
                                            emailIdToDomain=emailIdToDomain)
                filtered_mssg_list.append(mssg)
                if urls is not None:
                    all_urls.update(urls)
                print("------------------------------")
                # final_list.append(message_dic)  # This will create a dictonary item in the final list

                # This will mark the messagea as read
                # self.gmail.mark_as_read(m_id)
        print("Doing the batch jobs")

        print(len(all_urls))
        # unique_filename = "test/" + str(uuid.uuid4())
        # thefile = open(unique_filename, 'w')

        # for item in all_urls:
        #     thefile.write("%s\n" % item)

        print("Fav'ing all the urls")
        self.pocket.favourite(all_urls, 'g2p')

        print("Trashing all the emails from gmail now, got : " + str(len(filtered_mssg_list)))

        self.gmail.batch_trash_mail_given_raw_messages(filtered_mssg_list)

        # self.messageListToPocket(filtered_mssg_list, headersToExclude=headersToExclude, emailIdToDomain=emailIdToDomain)
