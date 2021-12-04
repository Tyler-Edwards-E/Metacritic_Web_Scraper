# Metacritic Web Scraper

##### This script takes a one or multiple Metacritic “list” pages and used 3 functions to parse through the list to collect review data on all the video games listed.
Metacritic has pages where they standardly list links to the pages of different games. 

Ex.] https://www.metacritic.com/browse/games/score/metascore/all/wii 

This web scraper is designed to utilize these lists, but the “parsePage” function can be used on any Metacritic video game page. The web scraper starts by taking one or multiple of these list URLs and parsing through and collecting the URLs for all the pages in the list using the “nextPageList” function.

Ex.] [“https://www.metacritic.com/browse/games/score/metascore/all/wii”, “https://www.metacritic.com/browse/games/score/metascore/all/wii?page=1”, “https://www.metacritic.com/browse/games/score/metascore/all/wii?page=2”,…]

After all URLs for each list page is collected, the “parseList” function collects all the URLs for the actual video game review pages from each list page. 

Ex.] [“https://www.metacritic.com/game/wii/super-mario-galaxy”, “https://www.metacritic.com/game/wii/super-mario-galaxy-2”, “https://www.metacritic.com/game/wii/the-legend-of-zelda-twilight-princess”,…]

Then the “parsePage” function goes through the collected game review pages and aggregates all the relevant data for each game and returns a dictionary that is added to a list of dictionaries. At the end of the loop, the list of dictionaries is turned into a pandas data frame which is then exported as a csv. 

###### Looping through the list pages twice is probably unnecessary and adds to the runtime, but it works well enough. [Metacritic’s robot.txt](https://www.metacritic.com/robots.txt) doesn’t mention anything about request time, but if you do request too much too fast the site will either temporarily block you or force you to slow down. There is a “time.sleep(1)” at the end of every loop to deal with this and keep the request speed consistent. If any data is not available on a page, that value is filled with a blank by default. Metacritic also has reviews for movies and TV shows, but the pages for these are different than the video game pages, so this web scraper can’t be applied for them.

A dataset made with this script has been uploaded to [Kaggle](https://www.kaggle.com/tyedwardse/metacritic-game-scores)
