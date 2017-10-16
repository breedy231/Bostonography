import csv
# https://github.com/mLewisLogic/foursquare
import foursquare
import logging
# https://github.com/googlemaps/google-maps-services-python
import googlemaps
# https://github.com/sixohsix/twitter
from TwitterSearch import *
from textblob import TextBlob
import requests
logging.basicConfig()


# Foursquare Block
fsquare = foursquare.Foursquare(
    client_id="D0XSLIQRKBTOI4CPXIX1SX4HUBSWW0T5NVBX4QB0GW5KNQWG",
    client_secret="F2OP2UBFX2MPNZPNQBQQDADXVOEMKQF4ZJVSWCTTXDXCSYXC",
    redirect_uri="https://is1500finproj-001654870.squarespace.com/")

# Google Maps Block
googlekey = "AIzaSyBfpncAwq6pxLJT4WpXE8zq92IMeHMqWR0"
gmaps = googlemaps.Client(key=googlekey)
bosGeocode = (42.3600825, -71.0588801)

# Twitter Block

ts = TwitterSearch(
    consumer_key="ZpFBUsdwZwcPtC748ObXZBZHs",
    consumer_secret="iLeQNYfAKcfCBkkSIrWOKeq10Rrmf26JquhRORT9oJNIph4goH",
    access_token="389720896-VnmsaBarHETYtABGMyYSsiItyRWsZXN9faZUxuEd",
    access_token_secret="tJXAQ4pZf8dtxSJwSJkpb1BDyP9EcGQFs91kWAj0JumoU"
)


class Restaurant:
    name = "No name"
    address = "No Address"
    tips = []
    geocode = (0,0)
    tweets = []
    grades = []
    sentiment = 0

    def __init__(self, name, address, grades):
        self.name = name
        self.address = address
        self.grades = grades


    def set_Geocode(self):
        response = gmaps.geocode(self.address)
        if len(response) == 0:
            pass
        else:
            location = response[0]['geometry']['location']
            self.geocode = (location['lat'], location['lng'])

    def set_Tips(self):
        newTips = []
        response = fsquare.venues.search(
            params={
                'near': 'Boston, MA',
                'query': self.name,
                'limit': 1
            }
        )
        if len(response['venues']) == 0:
            return
        else:
            ID = response['venues'][0]['id']
            tips = fsquare.venues.tips(
                ID, params={
                    'sort': 'recent',
                    'limit': 5})
        if len(tips['tips']['items']) == 0:
            newTips.append("No tips from Foursquare!")
        else:
            for row in tips['tips']['items']:
                newTips.append(row['text'])

        self.tips = newTips

    def set_Sentiment(self):
        total_sum = 0
        if len(self.tips) == 0:
            return
        else:
            for row in self.tips:
                blob = TextBlob(row)
                result = blob.sentiment.polarity
                total_sum += result
        total_avg = total_sum / len(self.tips)
        self.sentiment = total_avg

    def set_Tweets(self):
        tso = TwitterSearchOrder()
        tso.set_geocode(latitude=bosGeocode[0], longitude=bosGeocode[1], radius=25)
        tso.set_count(cnt=5)
        tso.add_keyword(word=self.name)
        response = ts.search_tweets(tso)
        self.tweets.append(response['content']['statuses'][0]['text'])


with open('only_a_b_c.csv', 'rU') as file:
    resReader = csv.reader(file, delimiter=',')
    rows = list(resReader)

print ('The file had {} rows'.format(len(rows)))

rowCount = len(rows)

rData = []
i = 0
for row in rows:
    rData.append(
        {'res'+str(i): Restaurant(row[0], row[1], row[2])})
    i += 1

k = 0
for x in range(len(rData)):
    curRestaurant = rData[x]['res'+str(x)]
    curRestaurant.set_Tips()
    curRestaurant.set_Sentiment()


j = 0
for row in rData:
    tipsStr = '; '.join(row['res' + str(j)].tips)
    newTips = tipsStr.replace(",", " ")

    print row['res'+str(j)].name + "," + \
          "'" + row['res'+str(j)].address + "'" + "," + \
          "'" + row['res'+str(j)].grades + "'" + "," + \
          "'" + newTips + "'" + "," + \
                str(row['res'+str(j)].sentiment)
    j += 1
