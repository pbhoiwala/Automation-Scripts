import urllib2
import random
from bs4 import BeautifulSoup
from slacker import Slacker

fileName = "values.txt"
with open(fileName) as f:
    content = f.readlines()
    inputs = [x.strip() for x in content]
    url_to_crawl = inputs[0]
    slack_api_token = inputs[1]
    slack_channel = inputs[2]
    slack_memebot_username = inputs[3]

memes = []
sent_memes = []
html = urllib2.urlopen(url_to_crawl)
soup = BeautifulSoup(html, "lxml")
slack = Slacker(slack_api_token)


def send_memes(meme_img_url):
    title = "Check out this meme"
    text_msg = "Time for some dank memes"
    attch = [{"title": title,
              "image_url": meme_img_url}]
    slack.chat.post_message(slack_channel, text_msg, username=slack_memebot_username, attachments=attch)


def crawl():
    img_tags = soup.findAll('img')
    for img in img_tags:
        temp = img.get('src')
        if temp[:1] != "/":
            meme_image_url = temp
            memes.append(meme_image_url)


def pick_memes_to_send():
    i = 0
    while i < 3:
        random_meme = random.choice(memes)
        if random_meme not in sent_memes and 'ifcdn' in random_meme:
            print(random_meme)
            send_memes(random_meme)
            sent_memes.append(random_meme)
            i += 1

if __name__ == '__main__':
    crawl()
    try:
        pick_memes_to_send()
        print("Successfully sent memes")
    except Exception as e:
        print(str(e))
        print("Unable to sent memes")
