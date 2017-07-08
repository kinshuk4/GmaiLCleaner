import requests
import color_util as cu
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def get_response_retries(url):
    s = requests.Session()

    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    s.mount('http://', HTTPAdapter(max_retries=retries))

    return s.get(url)


def get_contenttype_from_url(url):
    response = requests.get(url)
    return get_contenttype_from_response(response)


def get_contenttype_from_response(response):
    key_to_search = 'Content-Type'
    try:
        if key_to_search.lower() in response.headers:
            key_to_search = key_to_search.lower()
        maintype = response.headers[key_to_search].split(';')[0].lower()
        return maintype
    except Exception as e:
        cu.PrintInColor.red(str(e))
        print(response)
        return None


def is_valid_or_redirect_4_text(url):
    invalid_types = ('image/png', 'image/jpeg', 'image/gif', 'image/jpg')
    r = requests.get(url)
    correct_url, redirect_status = is_valid_or_redirect_from_response(r, url)

    if correct_url is not None:
        content_type = get_contenttype_from_response(r)

        if content_type in invalid_types:
            return None, False

    return correct_url, redirect_status


def is_valid_or_redirect_from_response(response, url):
    r = response
    if r.status_code is 200:
        return url, False
    elif r.status_code is 301:
        return r.history[0].headers['Location'], True
    else:
        return None, False


def is_valid_or_redirect(url):
    r = requests.get(url)
    return is_valid_or_redirect_from_response(r, url)


def is_redirect(url):
    r = requests.get(url)
    if r.history[0].status_code is 301:
        return True, r.history[0].headers['Location']
    else:
        return False, ''


def is_404(url):
    r = requests.get(url)
    if r.history[0].status_code is 301:
        return True

    return False


def check_all_redirects(url):
    try:
        r = requests.get(url)
        if len(r.history) < 1:
            print("Status Code: " + str(r.status_code))
        else:
            print("Status Code: 301. Below are the redirects")
            all_history = r.history
            i = 0
            for history in all_history:
                print("  " + str(i) + " - URL " + history.url + " - status " + str(history.status_code) + " - TO: " +
                      history.headers['Location'] + " \n")
                i += 1
    except requests.exceptions.MissingSchema:
        print("You forgot the protocol. http://, https://, ftp://")
    except requests.exceptions.ConnectionError:
        print("Sorry, but I couldn't connect. There was a connection problem.")
    except requests.exceptions.Timeout:
        print("Sorry, but I couldn't connect. I timed out.")
    except requests.exceptions.TooManyRedirects:
        print("There were too many redirects.  I can't count that high.")


def main():
    check_all_redirects('http://clicks.aweber.com/y/ct/?l=b7np2&m=3eztv74czdfmfpv&b=bua0bdhzhy_2zqfum4_zsg')


if __name__ == '__main__':
    main()
