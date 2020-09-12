import wx
import urllib.request
import io
import json
from itunesJSON import itunesJSON

# Pane pinging itunes
# lower right of window

def url_to_bmimg(img_url):
        buf = urllib.request.urlopen(img_url).read()
        sbuf = io.BytesIO(buf)
        return wx.Image(sbuf).ConvertToBitmap()

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='siren') #size=(400,500)
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)        

        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        self.my_btn = wx.Button(panel, label='Press Me')
        self.my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(self.my_btn, 0, wx.ALL | wx.CENTER, 5)        

        
        img = url_to_bmimg("https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/b9/ab/a7/b9aba7fd-bccd-9e84-8cc6-41f616ddb429/source/200x200bb.jpg")
        self.my_img_bitmap = wx.StaticBitmap(panel, -1, img, (10,10));
        my_sizer.Add(self.my_img_bitmap, 0, wx.ALL | wx.CENTER, 5) 


        fields_master = wx.BoxSizer(wx.HORIZONTAL)
        fields_left = wx.BoxSizer(wx.VERTICAL) 
        fields_right = wx.BoxSizer(wx.VERTICAL) 

        self.itunes_name = wx.TextCtrl(panel, size = (200,25))
        self.itunes_album = wx.TextCtrl(panel, size = (200,25))
        self.itunes_genre = wx.TextCtrl(panel, size = (200,25))
        self.itunes_artist = wx.TextCtrl(panel, size = (200,25))
        self.itunes_track = wx.TextCtrl(panel, size = (200,25))
        self.itunes_year = wx.TextCtrl(panel, size = (200,25))

        fields_left.Add(self.itunes_name, 0, wx.CENTER, 20)
        fields_left.Add(self.itunes_album, 0, wx.CENTER, 20)
        fields_left.Add(self.itunes_genre, 0, wx.CENTER, 20)
        fields_right.Add(self.itunes_artist, 0, wx.CENTER, 20)
        fields_right.Add(self.itunes_track, 0, wx.CENTER, 20)
        fields_right.Add(self.itunes_year, 0, wx.CENTER, 20)
        fields_master.Add(fields_left, 0, wx.CENTER, 20)
        fields_master.Add(fields_right, 0, wx.CENTER, 20)
        my_sizer.Add(fields_master, 0, wx.ALL | wx.CENTER, 5)    

        self.itunes_name.SetHint('Song')
        self.itunes_album.SetHint('Album')
        self.itunes_genre.SetHint('Genre')
        self.itunes_artist.SetHint('Artist')
        self.itunes_track.SetHint('Track Number')
        self.itunes_year.SetHint('Year')


        panel.SetSizer(my_sizer)      
        my_sizer.Fit(self)  
        self.Show()

    def on_press(self, event):
        value = self.text_ctrl.GetValue().replace(" ", "+")
        if value:
            self.itunes_json = itunesJSON(value)
            self.my_img_bitmap.SetBitmap(url_to_bmimg(self.itunes_json.get_image()))
            self.itunes_name.ChangeValue(self.itunes_json.get_track_name())
            self.itunes_album.ChangeValue(self.itunes_json.get_album())
            self.itunes_genre.ChangeValue(self.itunes_json.get_genre())
            self.itunes_artist.ChangeValue(self.itunes_json.get_artist())
            track_statement = "Hello! (_ out of _)"
            self.itunes_track.ChangeValue(track_statement)
            self.itunes_year.ChangeValue("We'll Figure it Out (year)")
            self.Refresh()
            
        else:
            print("Type something!")

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()