import urllib.request
import io
import json

class itunesJSON():
    def __init__(self, req):
        search_term = req.replace(" ", "+")
        ping_url = "https://itunes.apple.com/search?term=" + search_term + "&limit=10&entity=song"
        ituneURL = urllib.request.urlopen(ping_url)
        itunes_data = ituneURL.read()
        encoding = ituneURL.info().get_content_charset('utf-8')
        
        self.json = json.loads(itunes_data.decode(encoding))["results"]

    def get_image(self, json_index = 0, size = 200):
        self.img_url = self.json[json_index]["artworkUrl100"]
        replace_phrase = str(size) + "x" + str(size)
        self.img_url = self.img_url.replace("100x100", replace_phrase)
        return self.img_url

    def get_track_name(self, json_index = 0):
        return self.json[json_index]["trackName"]

    def get_artist(self, json_index = 0):
        return self.json[json_index]["artistName"]

    def get_album(self, json_index = 0):
        return self.json[json_index]["collectionName"]
        
    def get_genre(self, json_index = 0):
        return self.json[json_index]["primaryGenreName"]
    
    def get_track_num(self, json_index = 0):
        return self.json[json_index]["trackNumber"]
    
    def get_track_cnt(self, json_index = 0):
        return self.json[json_index]["trackCount"]

    def get_tracking(self, json_index = 0):
        return (self.get_track_num(json_index), self.get_track_cnt(json_index))

    
    
# audiofile.tag.images.remove(u'')
# audiofile.tag.images.set(1, imageArt , "image/jpeg" ,u"Description")

# test = itunesJSON("Location Khalid")
# print(test.get_track_name() + " by " + test.get_artist())
# print(test.get_album() + ", Track " + str(test.get_track_num()) + " of " + str(test.get_track_cnt()))
# print("Genre: " + test.get_genre())