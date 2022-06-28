from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import os
import glob


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


path="lyrics"
csv_files = glob.glob(os.path.join(path, "*.csv"))
to_conc = [pd.read_csv(file) for file in csv_files]
df = pd.concat(to_conc)
df.reset_index(drop=True, inplace=True)
df.insert(1,"songs","")


i = 0
for row in df["lyrics"]:
    if pd.notnull(row):
        lyr = row.replace("\n", " ")
        lyr = re.sub(r"(\d{0,2})Embed", "", lyr)
        nlyr = lyr.split("Lyrics", maxsplit=1)
        df["songs"][i]=nlyr[0]
        df["lyrics"][i]=nlyr[1]
    else: lyr = None
    i=i+1


df.to_csv("combined_lyrics.csv", index=False)