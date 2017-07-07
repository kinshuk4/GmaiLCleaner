def get_labels():
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
               'www.feedblitz.com/privacy', 'email.aytooweb.com/t', 'awealthofcommonsense.updatemyprofile.com',
               'http://msgservice.runtastic.com/unsubscribe/', 'http://link.runtastic.com/u/nrd.php', '/tag/',
               'http://email.mckinsey.com/T/v40000015cc6e879439386c8f4bbcfbb48/aec1b3cf7f944a450000021ef3a0bcdf/aec1b3cf-7f94-4a45-86db-eceda56f3a87',
               'http://email.mckinsey.com/T/v40000015cc6e879439386c8f4bbcfbb48/aec1b3cf7f944a450000021ef3a0bce0/aec1b3cf-7f94-4a45-86db-eceda56f3a87',
               'http://email.mckinsey.com/T/v40000015cc6e879439386c8f4bbcfbb48/aec1b3cf7f944a450000021ef3a0bcdc/aec1b3cf-7f94-4a45-86db-eceda56f3a87',
               'http://email.mckinsey.com/T/v40000015cc6e879439386c8f4bbcfbb48/aec1b3cf7f944a450000021ef3a0bcdd/aec1b3cf-7f94-4a45-86db-eceda56f3a87',
               'http://email.mckinsey.com/T/v40000015cc6e879439386c8f4bbcfbb48/aec1b3cf7f944a450000021ef3a0bcdc/aec1b3cf-7f94-4a45-86db-eceda56f3a87',
               'twitter.com/share', 'www.facebook.com/sharer/', 'wordpress/?elp=unsubscribe',
               'https://el2.convertkit-mail.com/c/gkuwq772f5hd2no8/3ydpyg/aHR0cDovL2xlb2JhYmF1dGEuY29t',
               'http://alphaideas.in/?author=1', 'w3.org/1999/xhtml', 'gravatar.com/avatar', 'amazon-adsystem',
               'blogger.com/rearrange', 'blogger.com/null', 'startupdigest.com/digests/youth'
               ]


def getPocketSenders():
    sender_set = {'Points and Figures <noreply+feedproxy@google.com>', 'Blogtrottr <busybee@blogtrottr.com>'
                  }
    header_set = {}
    return sender_set, header_set


POCKET_CLIENT_SECRET_FILE = "pocket_secret.json"
GMAIL_CLIENT_SECRET_FILE = "client_secret.json"
URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
HEADERS_TO_EXCLUDE = ['IndianWeb2.com', 'Indian Power Sector', 'OpIndia.com', 'Accommodation Times', 'Marc and Angel',
                      'RSSFODailyReport', 'BSE Notices', 'NSE News - Latest Financial Results', 'French Word-A-Day']

footer_finder_strings = ['You are receiving this email because you subscribed to this feed at',
                         'You are subscribed to email updates from'
                         'More Recent Articles - ', 'To Leave a Comment Click Here.',
                         'Click here to safely unsubscribe from', 'To stop receiving these emails, you may',
                         'unsubscribe from this list', 'WordPress.com | Thanks for flying with WordPress',
                         'subscribe-footer', 'To unsubscribe or change subscriber options visit',
                         'Manage Subscriptions', 'Contact Us']

careful_footer_strings = "Unsubscribe"

extensions_to_exclude = [".csv", ".dat", ".lst", ".zip", ".png", ".jpg", ".js", ".cms", ".dtd", '.gif']
characters_exclusion = ['#comments', '#respond']
DEBUG = False
EMAIL_ID_TO_DOMAIN_DIC = {"support@zenhabits.net": "https://zenhabits.net/",
                          "smallcapvaluefind@gmail.com": "http://smallcapvaluefind.blogspot.de/"}
