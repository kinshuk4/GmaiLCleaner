import sys
sys.path.append("/Users/kchandra/Lyf/Kode/SCM/Github/k2/GmaiLCleaner/moonpie")
import moonpie

sys.path.append("/Users/kchandra/Lyf/Kode/SCM/Github/k2/GmaiLCleaner/gmailclient")
import gmailclient

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

    def labelToPocket(self, labelIds, debug=False, headersToExclude=set(), emailIdToDomain={}):
        mssg_list = []
        for gmail_labels_ids in labelIds:
            curr_mssg_list = self.gmail.get_messages_for_labels(labelIds=gmail_labels_ids)
            mssg_list.extend(curr_mssg_list)

        final_list = []
        all_urls = set()
        all_ids = []
        message_dic = {}
        for mssg in mssg_list:
            m_id = mssg['id']  # get id of individual message
            all_ids.append(m_id)

            message_dic = self.gmail.get_message_data(m_id)
            if GmailPocket.exclude_message_on_subject(headersToExclude, message_dic['subject']):
                continue
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
                if known_senders_without_urls in message_dic['sender']:
                    url_from_domain = gcu.get_url_for_sender_email_id(known_senders_without_urls)
                    urls.extend(url_from_domain)

            print(message_dic['subject'])
            print(urls)
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
        self.pocket.favourite(all_urls, 'g2p')

        print("Trashing all the emails from gmail now")
        self.gmail.batch_trash_mail_given_raw_messages(mssg_list)