from bs4 import BeautifulSoup
import base64
import sys

sys.path.append("/Users/kchandra/Lyf/Kode/SCM/Github/k2/GmaiLCleaner/moonpie")
import moonpie
from moonpie.color_util import PrintInColor as pic

ALLOWED_SCOPES = ['https://mail.google.com/',
                  'https://www.googleapis.com/auth/gmail.compose',
                  'https://www.googleapis.com/auth/gmail.modify',
                  'https://www.googleapis.com/auth/gmail.send']

class GmailMessageUtil:
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
