from lru import LRUCacheDict

# TODO: Get all the message and we can do following with it:
# 1. process it and then
# 2a. archive it
# 2b. delete it
# 2c. do nohting - I will then manually do something about it

class MessageState:
    INIT = 0
    DONOTHING = 1
    ARCHIVE = 2
    DELETE = 3

class GmailMessage:
    def __init__(self, message_dic):
        self.message_dic = message_dic
        self.message_state = MessageState.INIT

class GmailProcessor:
    def __init__(self, , gmailClient):
        self.gmail = gmailClient
        self.cache = LRUCacheDict(max_size=16000, expiration=24 * 60 * 60)  # 24 h cache
        self.initialize()

    def initialize(self):
        labelIds = [['INBOX'], ['SPAM']]  #
        mssg_list = []
        for gmail_labels_ids in labelIds:
            curr_mssg_list = self.gmail.get_messages_for_labels(labelIds=gmail_labels_ids)
            mssg_list.extend(curr_mssg_list)


        for mssg in mssg_list:
            m_id = mssg['id']
            message_dic = self.gmail.get_message_data(m_id)

            # TODO: Now pass this message to different filters and mark for next step
            # is part of pocket filter
            # is part of time relevant like news etc. and 7 days old, delete it
            #