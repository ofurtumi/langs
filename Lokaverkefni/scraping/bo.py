import urllib3
import re

api = "https://www.guitarparty.com/api/v3/core/songs/"

def format_song(raw_song):
    song = re.sub(r"\[.*?\]", "", raw_song)
    song = re.sub(r"\{.*?\}", "", song)
    song = re.sub(r"\(.*?\)", "", song)
    song = re.sub(r" +", " ", song)
    song = [line.strip() for line in song.split("\n") if line.strip() != ""]
    return song

def get_song(song_id):
    id = "27049"
    page = urllib3.request("GET", api + id)
    data = page.json()
    song = format_song(data["song"])
    title = data["title"]
    return title, song

def get_ids():
    limit = 1859
    ids = []
    http = urllib3.PoolManager()
    for i in range(limit):
        url = api + f"?format=json&limit=10&offset={ i * 10 }"
        try:
            print(f"{i}/{limit - 1} - ids: {len(ids)}", end='\r')
            page = http.request("GET", url)
            data = page.json()
            new_ids = [song["id"] for song in data["results"] if song["language"] == "is"]
            if len(new_ids) != 0:
                ids = ids + new_ids

                # append to file
                with open("ids_10.txt", "a") as f:
                    f.write("\n")
                    f.write("\n".join(list(map(str, new_ids))))

        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            exit()
        except:
            print(f"Error: failed at offset {i}")

    return ids

ids = get_ids()
print(len(ids))

