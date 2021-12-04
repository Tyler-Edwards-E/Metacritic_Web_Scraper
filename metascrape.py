
# Metacritic Scrape
# Tyler Edwards
# tee24@drexel.edu
# 11-7-2021

import csv
import bs4
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
import time
import pandas as pd


def parsePage(URL):
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")

    header = page_soup.find("div", {"class" : "product_title"})
    details = page_soup.find("ul", {"class" : "summary_details"})
    summary = page_soup.find("div", {"class" : "summary_wrap"})

    game_title = ""
    platform = ""
    publisher = ""
    release_date = ""
    other_platforms = []
    metascore = ""
    metascore_N = ""
    userscore = ""
    userN = ""
    desc = ""
    developer = ""
    genre = ""
    playercount = ""
    ESRB = ""
    critic_scores = [0, 0, 0]
    user_scores = [0, 0, 0]
    URL = ""
    cs = None
    us = None


    critic_sentiment = page_soup.find("div", {"class" : "module reviews_module critic_reviews_module"})
    if critic_sentiment != None:
        cs = critic_sentiment.find("ol", {"class" : "score_counts hover_none"}).find_all("li", {"class" : "score_count"})
    user_sentiment = page_soup.find("div", {"class" : "module reviews_module user_reviews_module"})
    if user_sentiment.find("ol", {"class" : "score_counts hover_none"}) != None:
        us = user_sentiment.find("ol", {"class" : "score_counts hover_none"}).find_all("li", {"class" : "score_count"})

# Final Data
    game_title = header.find("a", {"class" : "hover_none"}).text.replace("\n", "")
    platform = header.find("span", {"class" : "platform"}).text.strip()
    if (details.find("li", {"class": "summary_detail publisher"}) != None):
        publisher = details.find("li", {"class": "summary_detail publisher"}).find("span", {"class" : "data"}).text.replace(" ", "").strip()
    if (details.find("li", {"class": "summary_detail release_data"}) != None):
        release_date = details.find("li", {"class": "summary_detail release_data"}).find("span", {"class" : "data"}).text.strip()
    if (details.find("li", {"class": "summary_detail product_platforms"}) != None):
        also_on = details.find("li", {"class": "summary_detail product_platforms"}).find_all("a", {"class" : "hover_none"}) # Platform list
        for i in also_on:
            other_platforms.append(i.text) # Platforms
    if (summary.find("span", {"itemprop" : "ratingValue"}) != None):
        metascore = summary.find("span", {"itemprop" : "ratingValue"}).text
    if (summary.find("span", {"class" : "count"}).find("a") != None):
        metascore_N = summary.find("span", {"class" : "count"}).find("a").text.strip().replace("\n","").replace("Critic Reviews", "") # Metascore reviews

    if (summary.find("div", {"class" : "metascore_w user large game mixed"}) != None):
        userscore = summary.find("div", {"class" : "metascore_w user large game mixed"}).text
    elif (summary.find("div", {"class" : "metascore_w user large game positive"}) != None):
        userscore = summary.find("div", {"class" : "metascore_w user large game positive"}).text
    elif (summary.find("div", {"class" : "metascore_w user large game negative"}) != None):
        userscore = summary.find("div", {"class" : "metascore_w user large game negative"}).text

    if summary.find("div", {"class" : "userscore_wrap feature_userscore"}).find("span", {"class" : "count"}).find("a") != None:
        userN = summary.find("div", {"class" : "userscore_wrap feature_userscore"}).find("span", {"class" : "count"}).find("a").text.replace("Ratings", "").strip()
    if (summary.find("span", {"class" : "blurb blurb_expanded"}) != None):
        desc = summary.find("span", {"class" : "blurb blurb_expanded"}).text
    elif (summary.find("li", {"class": "summary_detail product_summary"}) != None):
        desc = summary.find("li", {"class": "summary_detail product_summary"}).find("span", {"class" : "data"}).find("span").text
    if (summary.find("li", {"class" : "summary_detail developer"}) != None):
        developer = summary.find("li", {"class" : "summary_detail developer"}).find("span", {"class" : "data"}).text.strip()
    if (summary.find("li", {"class" : "summary_detail product_genre"}).find("span", {"class" : "data"}) != None):
        genre = summary.find("li", {"class" : "summary_detail product_genre"}).find("span", {"class" : "data"}).text.strip()
    if (summary.find("li", {"class" : "summary_detail product_players"}) != None):
        playercount = summary.find("li", {"class" : "summary_detail product_players"}).find("span", {"class" : "data"}).text.replace("Up to more than", "").strip()
    if (summary.find("li", {"class" : "summary_detail product_rating"}) != None):
        ESRB = summary.find("li", {"class" : "summary_detail product_rating"}).find("span", {"class" : "data"}).text.strip()

    if cs != None:
        critic_scores = []
        for i in cs:
            critic_scores.append(i.find("span", {"class" : "count"}).text.strip())
    if us != None:
        user_scores = []
        for i in us:
            user_scores.append(i.find("span", {"class" : "count"}).text.strip())

    URL = str(urlopen(req).geturl())

    data = {"game_title" : game_title, "platform" : platform,  "other_platforms" : other_platforms, "publisher" : publisher, "developer" : developer,
            "release_date" : release_date, "description" : desc, "genre" : genre, "ESRB_Rating" : ESRB, "multiplayer" : playercount,
            "metascore" : metascore, "num_meta_reviews" : metascore_N, "userscore" : userscore, "num_user_reviews" : userN,
            "critic_positive" : critic_scores[0], "critic_mixed" : critic_scores[1], "critic_negative" : critic_scores[2],
            "user_positive" : user_scores[0], "user_mixed" : user_scores[1], "user_negative" : user_scores[2], "URL" : URL}
    return data


def parseList(URL):
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")

    URL_List = []

    x = page_soup.find_all("a", {"class" : "title"})
    for i in x:
        print(i["href"]) # add metacritic.com
        URL_List.append(i["href"])

    return URL_List


def nextPageList(URL):
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")
    l = []
    if (page_soup.find("a", {"rel" : "prev"}) == None):
        print("Saving URL || " + str(urlopen(req).geturl()))
        l.append(str(urlopen(req).geturl()))
        #time.sleep(1)
    if (page_soup.find("a", {"rel" : "next"}) != None):
        y = page_soup.find("a", {"rel" : "next"})["href"]
        y = "https://www.metacritic.com" + y
        print("Saving URL || " + y)
        #time.sleep(1)
        l.append(y)
        l = l + nextPageList(y)
    return l

# ===============================================================================

start = time.time()

                #"https://www.metacritic.com/browse/games/release-date/available/ps5/metascore"
                #"https://www.metacritic.com/browse/games/release-date/available/ios/metascore"
                #"https://www.metacritic.com/browse/games/release-date/available/ps4/metascore",
                # "https://www.metacritic.com/browse/games/release-date/available/xbox-series-x/metascore",
                # "https://www.metacritic.com/browse/games/release-date/available/xboxone/metascore",
                # "https://www.metacritic.com/browse/games/release-date/available/switch/metascore",
                # "https://www.metacritic.com/browse/games/release-date/available/pc/metascore",
                # "https://www.metacritic.com/browse/games/release-date/available/ps3/metascore",
                # "https://www.metacritic.com/browse/games/release-date/available/ps2/metascore",
                # "https://www.metacritic.com/browse/games/release-date/available/ps1/metascore"

platform_list = ["https://www.metacritic.com/browse/games/release-date/available/ps/metascore",
                "https://www.metacritic.com/browse/games/release-date/available/xbox/metascore",
                "https://www.metacritic.com/browse/games/release-date/available/wii/metascore",
                "https://www.metacritic.com/browse/games/release-date/available/gamecube/metascore",
                "https://www.metacritic.com/browse/games/release-date/available/wii-u/metascore",
                "https://www.metacritic.com/browse/games/release-date/available/n64/metascore",
                "https://www.metacritic.com/browse/games/release-date/available/dreamcast/metascore"
                ]
page_list = []
game_list = []

d = []
print()
print("================================================================================================================")

print()

for i in platform_list:
    page_list = page_list + nextPageList(i)
    print("----------------------------------------------------------------------------------------------------------------")
    time.sleep(1)

for i in page_list:
    game_list = game_list + parseList(i)
    print("----------------------------------------------------------------------------------------------------------------")
    time.sleep(1)

for i in game_list:
    print("Collecting data from --> https://www.metacritic.com" + i)
    d.append(parsePage("https://www.metacritic.com" + i))
    print("----------------------------------------------------------------------------------------------------------------")
    time.sleep(1)

print()
print("Creating --> metascrape.csv")
df = pd.DataFrame(d)
df.to_csv("metascrape.csv", index=False, encoding='utf-8')
print()

end = time.time()

hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
print()
