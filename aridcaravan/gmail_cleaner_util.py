import os
import re
import sys

import config as conf
from aridcaravan import special_subscription as ssb

sys.path.append("/Users/kchandra/Lyf/Kode/SCM/Github/k2/GmaiLCleaner/moonpie")
from moonpie import request_util as ru, url_util as uu

def ignore_urls_from_set(input_urls):
    urls = set()
    if conf.DEBUG:
        print("++++++++ URL SET 0 - Remove all the urls as marked in the IGNORE URL")
    for url in input_urls:
        if not any(ignore_url in url.lower() for ignore_url in conf.IGNORE_URLS):
            urls.add(url)
        else:
            pass
            # print(url)

    # cleanup URLs
    cleanedup_urls = set()
    if conf.DEBUG:
        print("++++++++++URL SET 1 - Remove characters like # from the url")
    for url in urls:
        url_lower = url.lower()
        if conf.DEBUG:
            print(url_lower)

        for x in conf.characters_exclusion:
            if x in url_lower:
                url_lower = url_lower.split(x)[0]  # for example ignore the part after '#'
                cleanedup_urls.add(url_lower)
            else:
                cleanedup_urls.add(url_lower)
    # starting second set of rules
    all_urls_valid_for_pocket = []
    if conf.DEBUG:
        print("+++++++++++++++++++++++++ Got URL Set 2 +++++++++++++++++++++++++++")
    for url in cleanedup_urls:
        # url needs encoding
        if conf.DEBUG:
            print(url)
        if ';' in url:
            # url = uu.decode_url(url)
            # TODO for some reason decoding is not working and not replacing &amp; to &
            url = url.replace('&amp;', '&')
        if '"' in url:
            url = url.replace('"', '')

        if check_url(url):
            all_urls_valid_for_pocket.append(url)
    if conf.DEBUG:
        print("++++++++++++Now Visit the sites and start cleanup")
    all_urls_valid_for_pocket = cleanup_urls_after_visiting(all_urls_valid_for_pocket)
    return all_urls_valid_for_pocket


def cleanup_urls_after_visiting(input_urls):
    urls = set()
    for url in input_urls:
        if not (url.startswith("http://") or url.startswith("https://") or url.startswith("www")):
            url = "http://" + url
        correct_url, is_redirect = ru.is_valid_or_redirect_4_text(url)

        if correct_url is not None:
            urls.add(correct_url)

            if is_redirect:
                print(correct_url)
    return urls


def extract_urls_from_body(body):
    # sender_set, header_set = getPocketSenders()

    # print(subject)
    str_body = str(body)
    searched_urls = re.findall(conf.URL_REGEX, str_body)
    all_urls_valid_for_pocket = ignore_urls_from_set(searched_urls)
    return all_urls_valid_for_pocket


def check_url(url):
    url_lower = url.lower()
    url_without_query_param = uu.remove_query_params(url_lower)
    extension = os.path.splitext(url_without_query_param.rstrip('/'))[1]

    if extension in conf.EXCLUDED_EXTENSIONS:
        return False

    # if any(x in url_lower for x in conf.characters_exclusion):
    #     return False
    if url_lower is None:
        print(url_lower)
    if uu.check_if_only_domain_name(url_lower):
        return False
    if uu.is_social_media_profile(url):
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


def get_url_for_sender_email_id(email_id):
    url = ssb.get_post_from_blog(conf.EMAIL_ID_TO_DOMAIN_DIC[email_id])

    return ignore_urls_from_set([url])
