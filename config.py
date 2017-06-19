
def getLabels():
    ## Choose labels
    label_id_one = 'INBOX'
    label_id_two = 'UNREAD'
    label_id_three = 'SPAM'
    label_id_four = 'Label_181'
    return [[label_id_four], [label_id_three, label_id_four]]


user_id = 'me'
IGNORE_URLS = ['feedburner.google.com/fb/a/mailunsubscribe?', 'subscribe.wordpress.com', 'www.aweber.com',
               'blogtrottr.com/unsubscribe/', 'blogtrottr.com/subscriptions', 'blogtrottr.com',
               'capitalideasonline.com/wordpress/?elp=unsubscribe', 'u2651907.ct.sendgrid.net/wf/click?upn',
               'email.aytooweb.com/t', 'thebigpicture.updatemyprofile.com',
               'whitecoatinvestor.us4.list-manage.com/vcard?u=106bf0eb2d98400b0754830dc&id=6ce0a43a91', '/profile?u',
               '/unsubscribe?u', 'financialexpress', 'nseindia.com', 'bseindia.com', 'gurufocus.com',
               'email.seekingalpha.com/account/unsubscribe', 'app.feedblitz.com', 'archive.feedblitz.com',
               'www.feedblitz.com/privacy']





def getPocketSenders():
    sender_set = {'Points and Figures <noreply+feedproxy@google.com>', 'Blogtrottr <busybee@blogtrottr.com>'
                  }
    header_set = {}
    return sender_set, header_set


POCKET_CONSUMER_KEY=""
POCKET_ACCESS_TOKEN=""
GMAIL_CLIENT_SECRET_FILE="client_secret.json"