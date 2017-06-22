def main():
    pass


def remove_protocol_from_url(url):
    url_lower = url.lower()
    without_http = url_lower.replace("http://", "")
    without_http = without_http.replace("https://", "")
    return without_http


def check_if_only_domain_name(url):
    url_lower = url.lower()
    without_http = remove_protocol_from_url(url_lower)
    without_http = without_http.strip("/")
    parts = without_http.split('/')
    if len(parts) < 2:
        return True
    return False


def is_twitter_user_url(url):
    url_lower = url.lower()
    without_http = remove_protocol_from_url(url_lower)
    without_twitter = without_http.replace("twitter.com/", "")
    only_user = without_twitter.split('/')
    if len(only_user) == 1:
        return True

    return False

if __name__ == '__main__':
    main()
