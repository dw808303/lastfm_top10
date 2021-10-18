#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# <bitbar.title>Rolling Top 10 Artists</bitbar.title>
# <bitbar.version>1.1.1</bitbar.version>
# <bitbar.author>d.w.</bitbar.author>
# <bitbar.author.github>dw808303</bitbar.author.github>
# <bitbar.image>https://www.freeke.org/i/2021/top10.jpg</bitbar.image>
# <bitbar.dependencies>python3, requests</bitbar.dependencies>
# <bitbar.desc>Most played artists this week, via last.fm</bitbar.desc>

# constants (must edit these)
# please create a last.fm API key at https://www.last.fm/api/account/create
# this script hits the last.fm API endpoint 3 times, so keep that in
# mind when deciding how frequently to invoke it w/ swiftbar/xbar

lastfmUsername = ""
lastfmAPIKey = ""

# shouldn't need to edit past this point

import requests
import time
import sys

# Draw menubar icon (uses SFSymbols)

print ("􀓵")
print ("---")


# query last.fm for the artist list

my_endpoint = "%s%s%s%s%s" % ("http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=",
                               lastfmUsername,
                               "&api_key=",
                               lastfmAPIKey,
                               "&format=json&period=7day&limit=10")

try:
    r = requests.get(my_endpoint)
except:
    print ("Problem retrieving data from last.fm")
    sys.exit(-1)

try:
    artistDict = r.json()
except:
    print ("Couldn't decode last.fm response")
    sys.exit (-2)
    
for i in range(10):
    print ('{} ({})|href={}'.format(
    artistDict["topartists"]["artist"][i]["name"],
    artistDict["topartists"]["artist"][i]["playcount"],
    artistDict["topartists"]["artist"][i]["url"]
    ))

# Compute number of tracks 
# a) scrobbled today
# b) scrobbled this week
# not y2038 compliant

sse = int(time.time())
yesterday = sse - 86400
lastweek = sse - 604800

recenttracksendpoint = "%s%s%s%s%s" % ("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=",
                                       lastfmUsername,
                                       "&api_key=",
                                       lastfmAPIKey,
                                       "&format=json")

daypoint = ('{}{}{}'.format(recenttracksendpoint,"&from=",yesterday))
weekpoint = ('{}{}{}'.format(recenttracksendpoint,"&from=",lastweek))

r = requests.get(daypoint)
daytrax = r.json()['recenttracks']['@attr']['total']

r = requests.get(weekpoint)
weektrax = r.json()['recenttracks']['@attr']['total']

print ("---")
print ('{} {}'.format("Played Today:",daytrax))
print ('{} {}'.format("Played This Week:",weektrax))

print("---")
print("%s%s" % ("last.fm Profile |href=https://www.last.fm/user/",
                 lastfmUsername))
