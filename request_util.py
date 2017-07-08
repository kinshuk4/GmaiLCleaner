import requests
import color_util as cu


def is_valid_or_redirect(url):
    r = requests.get(url)
    if r.status_code is 200:
        return url, False
    elif r.status_code is 301:
        return r.history[0].headers['Location'], True
    else:
        return None, False


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
