import json, requests, os
from dotenv import load_dotenv

HOST = 'https://im.smsclub.mobi/sms/'
env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)

class HTTPError(Exception):
    pass


class SmsClient(object):

    def __init__(self, token):
        self.token = token

    def make_request(self, url_req, body=None):
        #connection = http.client.HTTPSConnection(HOST, port=443)
        url = HOST+url_req

        headers = {'Authorization': 'Bearer {}'.format(self.token),
                   'Content-type': 'application/json'}
        if body:
            body = json.dumps(body)

        try:
            response = requests.post(url, data=body, headers=headers)
            balance_data = response.json()
        except:
            balance_data = None

            print("Запрос на сервер SMSclub непрошел!")
       # connection.request(method, url, body=body, headers=headers)
       #  response = connection.getresponse()
       #  if response.status != 200:
       #      raise HTTPError('{}: {}'.format(response.status, response.reason))

        # response_data = response.read()
        return balance_data
    def getBalanceSms(self):
        url = "balance"
        return self.make_request(url)
    def getStatusSms(self, data):
        url = "status"
        body = data
        return self.make_request(url, body)
    def getSendSms(self, data):
        url = "send"
        body = data
        return self.make_request(url, body)



def AuthToken():
    AUTH_TOKEN = os.getenv("SMS_TOKEN")
    # Initialize Client
    if not AUTH_TOKEN:
        raise Exception('Sorry, there\'s no any AUTH_TOKEN!')

    api_example = SmsClient(AUTH_TOKEN)
    return api_example

def WriteBalanceSms():
    api_example = AuthToken()
    balance = api_example.getBalanceSms()
    # if not order_list['orders']:
    #     raise Exception('Sorry, there\'s no any order!')
    # with open("balance_sms.json", 'w', encoding='utf-8') as file:
    #    json.dump(balance, file, indent=4, ensure_ascii=False)
    return balance

def WriteStatusSms(data):
    api_example = AuthToken()
    status = api_example.getStatusSms(data)
    # if not order_list['orders']:
    #     raise Exception('Sorry, there\'s no any order!')
    # with open("status_sms.json", 'w', encoding='utf-8') as file:
    #    json.dump(status, file, indent=4, ensure_ascii=False)

def WriteSendSms(data):
    api_example = AuthToken()
    sendSms = api_example.getSendSms(data)
    # with open("send_sms.json", 'w', encoding='utf-8') as file:
    #    json.dump(sendSms, file, indent=4, ensure_ascii=False)

