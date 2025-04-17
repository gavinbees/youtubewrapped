from bs4 import BeautifulSoup
import os
import json
from googleapiclient.discovery import build

API_KEY = "API_LEY_HERE"
CLIENT_ID = "CLIENT_ID_HERE"
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_ids():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path = current_directory+"\\Takeout\\YouTube and YouTube Music\\history\\watch-history.html"
    f = open(path, "r", encoding="utf8")
    soup = BeautifulSoup(f, "html.parser") #soup object
    f.close()
    videos = soup.findAll("div", attrs={"class":"content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"}) #the actual content of a message
    ids = []
    for video in videos:
        id = str(video)[123:134]
        ids.append(id)
    return ids

def formulate_tags(ids):
    id_counter = {}
    for id in ids: #get each video id
        video_tags = get_tags(get_dict(id, False)) #get the list of tags for that video
        for tag in video_tags:
            if tag not in id_counter.keys():
                id_counter[tag] = 1
            else:
                id_counter[tag] +=1
    return id_counter
        
              

def get_tags(response): #pass in video dictionary
    try:
        try:
            tags = response["items"][0]["snippet"]["tags"]
            return tags
        except IndexError as ind_err:
            return []
    except KeyError as key_err:
        return []

def get_dict(video_id, save_json = False): #returns the dictionary with video info
    
    request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )

    response = request.execute() #response is a dictionary
    if save_json:
        with open(video_id+".json", "w") as file:
            json.dump(response, file, indent=4)
    return response

def main():
    id_counter = formulate_tags(get_video_ids())
    id_counter = {x: y for x, y in sorted(id_counter.items(), key=lambda item: item[1])}
    print(id_counter)

if __name__ == "__main__":
    main()

