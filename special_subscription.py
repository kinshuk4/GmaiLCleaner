import urllib.request as ur
from bs4 import BeautifulSoup
import config as conf
import url_util as uu


def main():
    print(get_post_from_blog('https://zenhabits.net/'))


def get_all_urls(url):
    response = ur.urlopen(url)
    soup = BeautifulSoup(response.read())
    urls = []
    for a in soup.findAll('a'):
        urls.append(a['href'])
    return urls


def get_post_from_blog(url):
    response = ur.urlopen(url)
    soup = BeautifulSoup(response.read(), "lxml")
    for a in soup.findAll('a', href=True):
        try:
            extracted_url = a.get('href').lower()
        except Exception as e:
            print(e)

        print(extracted_url)
        if uu.check_if_only_domain_name(extracted_url):
            continue
        if uu.is_twitter_user_url(extracted_url):
            continue
        if 'feedburner' in extracted_url:
            continue
        if 'blogger.com' in extracted_url:
            continue
        return extracted_url

    return ''


if __name__ == '__main__':
    main()
