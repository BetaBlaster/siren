import wx
import eyed3
import urllib.request
import io
import os
import json

# pane loading local file metadata
# lower left of window

class LocalFilePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        overall_sizer = wx.BoxSizer(wx.VERTICAL)

        self.missing_img = wx.Bitmap(os.getcwd() + "/missing.jpg")

        self.mp3_obj = eyed3.load(os.getcwd() + "/test.mp3")

        
        self.img_bitmap = wx.StaticBitmap(self, -1, self.missing_img, (10,10));
        self.update_image() ######### TO REMOVE?
        

        overall_sizer.Add(self.img_bitmap, 0, wx.ALL | wx.CENTER, 5)     
           
        fields_master = wx.BoxSizer(wx.HORIZONTAL)
        fields_left = wx.BoxSizer(wx.VERTICAL) 
        fields_right = wx.BoxSizer(wx.VERTICAL) 

        self.current_name = wx.TextCtrl(self, style = wx.TE_READONLY, size = (200,25))
        self.current_album = wx.TextCtrl(self, style = wx.TE_READONLY, size = (200,25))
        self.current_genre = wx.TextCtrl(self, style = wx.TE_READONLY, size = (200,25))
        self.current_artist = wx.TextCtrl(self, style = wx.TE_READONLY, size = (200,25))
        self.current_track = wx.TextCtrl(self, style = wx.TE_READONLY, size = (200,25))
        self.current_year = wx.TextCtrl(self, style = wx.TE_READONLY, size = (200,25))

        fields_left.Add(self.current_name, 0, wx.CENTER, 20)
        fields_left.Add(self.current_album, 0, wx.CENTER, 20)
        fields_left.Add(self.current_genre, 0, wx.CENTER, 20)
        fields_right.Add(self.current_artist, 0, wx.CENTER, 20)
        fields_right.Add(self.current_track, 0, wx.CENTER, 20)
        fields_right.Add(self.current_year, 0, wx.CENTER, 20)
        fields_master.Add(fields_left, 0, wx.CENTER, 20)
        fields_master.Add(fields_right, 0, wx.CENTER, 20)
        overall_sizer.Add(fields_master, 0, wx.ALL | wx.CENTER, 5)


        self.current_name.SetHint('Song')
        self.current_album.SetHint('Album')
        self.current_genre.SetHint('Genre')
        self.current_artist.SetHint('Artist')
        self.current_track.SetHint('Track Number')
        self.current_year.SetHint('Year')

        self.SetSizer(overall_sizer)


        self.update_text() ######### TO REMOVE?

    def load_file(self, path):
        self.mp3_obj = eyed3.load(path)
        self.update_text()
        self.update_image()
    
    def update_text(self):
        if self.mp3_obj.tag.title: self.current_name.ChangeValue(self.mp3_obj.tag.title)
        if self.mp3_obj.tag.album: self.current_album.ChangeValue(self.mp3_obj.tag.album)
        if self.mp3_obj.tag.genre: self.current_genre.ChangeValue(str(self.mp3_obj.tag.genre)) #See whats up with this; maybe list of genres
        if self.mp3_obj.tag.artist: self.current_artist.ChangeValue(self.mp3_obj.tag.artist)
        test_track = str(self.mp3_obj.tag.track_num[0]) + " of " + str(self.mp3_obj.tag.track_num[1]) if self.mp3_obj.tag.track_num else ""
        self.current_track.ChangeValue(test_track) 
        self.current_year.ChangeValue("Will be added eventually")

    def update_image(self):
        if self.mp3_obj.tag.images:
            img = io.BytesIO(self.mp3_obj.tag.images[0].image_data)
            self.mp3_img = wx.Image(img).Scale(200, 200).ConvertToBitmap()
            self.img_bitmap.SetBitmap(img)
        else:
            self.img_bitmap.SetBitmap(self.missing_img) 

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='siren', size=(400,400))
        panel = LocalFilePanel(self)
        
        self.Show()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()