import urllib2
import random
from bs4 import BeautifulSoup
from slacker import Slacker

fileName = "values.txt"
memes = []
sentMemes = []

with open(fileName) as f:
    content = f.readlines()
    inputs = [x.strip() for x in content]
    url_to_crawl = inputs[0]
    slack_api_token = inputs[1]
    slack_channel = inputs[2]
    slack_memebot_username = inputs[3]
    print(inputs)
html = urllib2.urlopen(url_to_crawl)
soup = BeautifulSoup(html, "lxml")
slack = Slacker(slack_api_token)


def sendMemeToSlack(memeImageUrl):
    title = "Check out this meme"
    textMsg = "Time for some dank memes"
    attch = [{"title": title,
              "image_url": memeImageUrl}]
    slack.chat.post_message(slack_channel, textMsg, username=slack_memebot_username, attachments=attch)


def crawl(memeSiteUrl):
    imgTags = soup.findAll('img')
    for img in imgTags:
        temp = img.get('src')
        if temp[:1] != "/":
            memeImageUrl = temp
            #print(memeImageUrl)
            memes.append(memeImageUrl)


def pickAndSendMemes():
    i=0
    while(i<3):
        randomMeme = random.choice(memes)
        if randomMeme not in sentMemes and 'ifcdn' in randomMeme:
            sentMemes.append(randomMeme)
            print(i, randomMeme)
            i += 1
            sendMemeToSlack(randomMeme)

crawl(url_to_crawl)
try:
    pickAndSendMemes()
    print("Successfully sent memes")
except:
    print("Unable to sent memes")

