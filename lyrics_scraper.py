from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

link_list=[]
lyrics_list=[]
albums_list=[]

html_links = requests.get("http://www.songlyrics.com/car-seat-headrest-lyrics/").text
soup_links = BeautifulSoup(html_links, "lxml")


links = soup_links.find_all("a", itemprop="url")
for link in links:
    html_text = requests.get(link.get("href")).text
    soup = BeautifulSoup(html_text, "lxml")
    text = soup.find("div", {"id": "songLyricsDiv-outer"})
    x = text.text.replace("\n"," ")
    x = x.replace("\r", " ")
    lyrics_list.append(x)



d={"lyrics":lyrics_list}

lyrics_data=pd.DataFrame(d)

lyrics_data.to_csv("lyrics.csv", index=False)


