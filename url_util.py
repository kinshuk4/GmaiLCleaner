import urllib.request as ur


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


def if_normal_social_url(url, domain_name):
    url_lower = url.lower()
    without_http = remove_protocol_from_url(url_lower)
    without_twitter = without_http.replace(domain_name + "/", "")
    only_user = without_twitter.split('/')
    if len(only_user) == 1:
        return True

    return False


def is_twitter_user_url(url):
    return if_normal_social_url(url, "twitter.com")


def is_fb_user_url(url):
    return if_normal_social_url(url, "www.facebook.com")


def is_social_media_profile(url):
    return is_twitter_user_url(url) or is_fb_user_url(url)


def remove_query_params(url):
    url_without_query_param = url.split('?')[0]
    url_without_query_param = url_without_query_param.split('&')[0]
    return url_without_query_param


def encode_url(url):
    return ur.quote(url)


def decode_url(url):
    return ur.unquote(url)


if __name__ == '__main__':
    main()
