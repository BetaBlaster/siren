import wx
import eyed3
import urllib.request
import io
import os
import json

# pane loading local file metadata
# lower left of window


# EVT_TEXT: Respond to a wxEVT_TEXT event, generated when the text changes.
# Notice that this event will be sent when the text controls contents changes – wx.TextCtrl.SetValue is called);

# GOOD FOR EVENT HANDLING AFTER STUFF IS CHANGED


def get_itunes(search_term):
    ping_url = "https://itunes.apple.com/search?term=" + search_term + "&limit=10&entity=song"
    ituneURL = urllib.request.urlopen(ping_url)
    itunes_data = ituneURL.read()
    encoding = ituneURL.info().get_content_charset('utf-8')
    return json.loads(itunes_data.decode(encoding))

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='siren') #size=(400,500)
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)        

        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)      


        mp3_object = eyed3.load(os.getcwd() + "/test.mp3")
        img = io.BytesIO(mp3_object.tag.images[0].image_data)
        img = wx.Image(img).Scale(200, 200).ConvertToBitmap()

        self.my_img_bitmap = wx.StaticBitmap(panel, -1, img, (10,10));
        my_sizer.Add(self.my_img_bitmap, 0, wx.ALL | wx.CENTER, 5)        
        self.current_name = wx.TextCtrl(panel)
        self.current_artist = wx.TextCtrl(panel)
        my_sizer.Add(self.current_name, 0, wx.CENTER, 20)
        my_sizer.Add(self.current_artist, 0, wx.CENTER, 20)
        title = mp3_object.tag.title

        self.current_name.ChangeValue(title)
        self.current_artist.ChangeValue(mp3_object.tag.artist)




        panel.SetSizer(my_sizer)      
        my_sizer.Fit(self)  
        self.Show()

    def on_press(self, event):
        value = self.text_ctrl.GetValue().replace(" ", "+")
        if value:
            self.itunes_json = itunesJSON(value)
            self.my_img_bitmap.SetBitmap(url_to_bmimg(self.itunes_json.get_image()))
            
            self.Refresh()
            
        else:
            print("Type something!")

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()