import json 
import requests
import time

TOKEN = "402164455:AAE4UsH3YJXdWoNrKApiDKEXWHUmWV1jxik"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=50"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

# def get_updates(offset=None):
#     url = URL + "getUpdates"
#     if offset:
#         url += "?offset={}".format(offset)
#     js = get_json_from_url(url)
#     return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates['result']:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def echo_all(updates):
    for update in updates['result']:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print e

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def buy(text):
    return text + " Khareedega bc!!"

def send_message(text, chat_id):
    firstWord = text.split()[0].upper()
    if firstWord == "NEWS":
        responseText = "AAj ki taza khabar"
    elif firstWord == "JOKE" or firstWord == "JOKES":
        responseText = "Joke maregaa bc!"
    elif firstWord == "WEATHER":
        responseText = "BAARISH AAYEGI BC"
    elif firstWord == "BUY":
        try:
            responseText = buy(text.split(' ', 1)[1])
            print responseText.split()[1:]
        except:
            responseText = "Buy What bc?"
    else:
        tu = "TU"
        if text.split()[0].upper() == tu.upper():
            responseText = text.upper()
        else: 
            responseText = "Tu " + text.upper() + " bc!!"


    # if text == 'joke':
    #     # Logic to send joke
    # elif text == 'news':
    #     # Logic to send joke
    # else:
    #     
    

    url = URL + "sendMessage?text={}&chat_id={}".format(responseText, chat_id)
    get_url(url)
    

def main():
    last_update_id = None
    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()