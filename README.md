# GmaiLCleaner
Cleaning my gmail on the go - using basic rules

Some of the rules I am following:

1. Get all the urls from the emails tagged as c_financial from gmail AND put them to Pocket and then delete them.
   IF you want to just read them, then just change the api.


## Dependencies

- Python 3
- Gmail api client
- Pocket api client

On your python virtual environment run this to get all the dependencies.

```pip install -r requirements.txt```


## Gmail Api

The API’s wizard comes handy to create the project, get credentials, and authenticate them. However, the process that should be followed after that is not mentioned clearly.

Before running this script, the user should get the authentication by following 
the [Gmail API link](https://developers.google.com/gmail/api/quickstart/python).
Also, client_secret.json should be saved in the same directory as this file. Don't checkin it into the github. 

#### Step by Step Guide

1. Install requirements ($ pip3 install -r requirements.txt). Currently it has only google-api-python-client.
2. Go to Google APIs: [https://console.developers.google.com/iam-admin/projects](https://console.developers.google.com/iam-admin/projects)
3. Go Project > Create project
4. Give the project a name and wait for Google to create the project
5. From the list of APIs in the library, select 'Gmail API' and on the next screen click 'Enable'
6. On the left-hand side, click 'Credentials'
7. Click Create credentials > OAuth client ID
8. Click 'Configure consent screen'
9. Enter a Product Name and click save
10. Under 'client ID' choose other. I'm not sure what this is for, I used my project name
11. Click 'OK' to get rid of the popup
12. Click the download icon and save the file to somewhere in your project - rename it, e.g. 'client_secret.json'
13. Add the python-gmail-api code to your project.
14. Modify the following as required: CLIENT_SECRET_FILE, CREDENTIAL_FILE, APPLICATION_NAME, MANUAL_AUTH
15. The first time you call the code, you will be asked to go to a URL and after authenticating, the information will be saved in storage.json

#### Api Reference

[Here](https://developers.google.com/gmail/api/v1/reference/) is the api reference.

TODO: Gmail message format.

## Pocket Api
This package provides a wrapper class around GetPocket V3 APIs.

### Installation

```
pip install pocket-api
```

### Usage

First, you have to [Create your consumer key](https://getpocket.com/developer/apps/new) from getpocket's developer console. To get the access token, you have to authorize the app on your own account. There are tools on the web that can automate this for you such as [fxneumann's OneClickPocket](http://reader.fxneumann.de/plugins/oneclickpocket/auth.php)

Pocket api used: https://github.com/rakanalh/pocket-api

#### Updating the pocket_secret.json
The pocket json file format:
```json
{
  "consumer_key" : "<Your consumer key>",
  "access_token" : "<Your access token>"
}
```
Please put your consumer key and access token and that should be all.


### Disclaimer
The information and code in these repositories was placed here for my own use but are released into the public domain in the hopes that they might be useful to others. Where I have used information from others I have tried to use and attribute it properly.

I make no guarantees or warrantees of any kind about the suitability for any project or use. None of it has received testing or certification for a particular use.

#### Credit

https://github.com/abhishekchhibber/Gmail-Api-through-Python/

https://github.com/chris-brown-nz/python-gmail-api

https://github.com/rakanalh/pocket-api

https://github.com/tapanpandita/pocket

https://github.com/NadalVRoMa/Emilidos/blob/2668024f6684724ce123802de5b6c1148bc7751c/main.py

https://github.com/amitkmr/Terminal-Geek/blob/9388cea460ffdc5638841e98bd9c2fd9838dbf15/Terminal%20Gmail/gmail.py