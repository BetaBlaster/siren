import wx
import eyed3
import urllib.request
import io
import os
import json

# pane loading local file metadata
# lower left of window


class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='siren') #size=(400,500)
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)           


        # Make into function
        mp3_object = eyed3.load(os.getcwd() + "/test.mp3")
        img = io.BytesIO(mp3_object.tag.images[0].image_data) # If no images, load pic i make
        img = wx.Image(img).Scale(200, 200).ConvertToBitmap()

        my_img_bitmap = wx.StaticBitmap(panel, -1, img, (10,10));
        my_sizer.Add(my_img_bitmap, 0, wx.ALL | wx.CENTER, 5)     
           
        fields_master = wx.BoxSizer(wx.HORIZONTAL)
        fields_left = wx.BoxSizer(wx.VERTICAL) 
        fields_right = wx.BoxSizer(wx.VERTICAL) 

        self.current_name = wx.TextCtrl(panel, style = wx.TE_READONLY, size = (200,25))
        self.current_album = wx.TextCtrl(panel, style = wx.TE_READONLY, size = (200,25))
        self.current_genre = wx.TextCtrl(panel, style = wx.TE_READONLY, size = (200,25))
        self.current_artist = wx.TextCtrl(panel, style = wx.TE_READONLY, size = (200,25))
        self.current_track = wx.TextCtrl(panel, style = wx.TE_READONLY, size = (200,25))
        self.current_year = wx.TextCtrl(panel, style = wx.TE_READONLY, size = (200,25))

        fields_left.Add(self.current_name, 0, wx.CENTER, 20)
        fields_left.Add(self.current_album, 0, wx.CENTER, 20)
        fields_left.Add(self.current_genre, 0, wx.CENTER, 20)
        fields_right.Add(self.current_artist, 0, wx.CENTER, 20)
        fields_right.Add(self.current_track, 0, wx.CENTER, 20)
        fields_right.Add(self.current_year, 0, wx.CENTER, 20)
        fields_master.Add(fields_left, 0, wx.CENTER, 20)
        fields_master.Add(fields_right, 0, wx.CENTER, 20)
        my_sizer.Add(fields_master, 0, wx.ALL | wx.CENTER, 5)     

        self.current_name.SetHint('Song')
        self.current_album.SetHint('Album')
        self.current_genre.SetHint('Genre')
        self.current_artist.SetHint('Artist')
        self.current_track.SetHint('Track Number')
        self.current_year.SetHint('Year')

        self.current_name.ChangeValue(mp3_object.tag.title)
        self.current_album.ChangeValue(mp3_object.tag.album)
        self.current_genre.ChangeValue(str(mp3_object.tag.genre)) #See whats up with this; maybe list of genres
        self.current_artist.ChangeValue(mp3_object.tag.artist)
        test_track = str(mp3_object.tag.track_num[0]) + " of " + str(mp3_object.tag.track_num[1])
        self.current_track.ChangeValue(test_track) 
        self.current_year.ChangeValue("Will be added eventually")

        

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