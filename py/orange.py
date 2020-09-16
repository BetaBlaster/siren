import wx
import urllib.request
import io
import json
from itunesJSON import itunesJSON
from TrackTextBox import TrackTextBox

# Pane pinging itunes
# lower right of window

# EVT_TEXT: Respond to a wxEVT_TEXT event, generated when the text changes.
# Notice that this event will be sent when the text controls contents changes – wx.TextCtrl.SetValue is called);

# GOOD FOR EVENT HANDLING AFTER STUFF IS CHANGED (make save button bottom right clickable)

def url_to_bmimg(img_url):
        buf = urllib.request.urlopen(img_url).read()
        sbuf = io.BytesIO(buf)
        return wx.Image(sbuf).ConvertToBitmap()

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='siren') #size=(400,500)
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)      

        search_master = wx.BoxSizer(wx.VERTICAL)
        search_searcher = wx.BoxSizer(wx.HORIZONTAL)

        self.text_ctrl = wx.TextCtrl(panel, style = wx.TE_PROCESS_ENTER, size = (300,25)) #add bind for pressing enter
        self.text_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_press_search)
        search_searcher.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        self.my_btn = wx.Button(panel, label='Search')
        self.my_btn.Bind(wx.EVT_BUTTON, self.on_press_search)
        search_searcher.Add(self.my_btn, 0, wx.ALL | wx.CENTER, 5)   
        search_master.Add(search_searcher, 0, wx.ALL | wx.CENTER, 5)   

        ### second row of search area - left+right buttons #
        search_selection = wx.BoxSizer(wx.HORIZONTAL)
        but_left = wx.Button(panel, label='left')
        but_left.Bind(wx.EVT_BUTTON, self.press_choice_left)
        search_selection.Add(but_left, 1, wx.ALL | wx.CENTER, 5)   
        self.search_index = 0
        self.json_selected = wx.StaticText(panel, label="0 of 0")
        search_selection.Add(self.json_selected, 1, wx.LEFT | wx.RIGHT | wx.CENTER, 30)   
        but_right = wx.Button(panel, label='right')
        but_right.Bind(wx.EVT_BUTTON, self.press_choice_right)
        search_selection.Add(but_right, 1, wx.ALL | wx.CENTER, 5) 
        search_master.Add(search_selection, 0, wx.CENTER)
        my_sizer.Add(search_master, 0, wx.ALL | wx.CENTER, 5)    


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
        self.itunes_track = TrackTextBox(panel, True).getTB() #wx.TextCtrl(panel, size = (200,25))
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
        # self.itunes_track.SetHint('Track Number')
        self.itunes_year.SetHint('Year')


        panel.SetSizer(my_sizer)      
        my_sizer.Fit(self)  
        self.Show()

    def update_search(self):

            self.json_selected.SetLabel(str(self.search_index + 1) + " out of " + str(self.itunes_json.length))
        
            self.my_img_bitmap.SetBitmap(url_to_bmimg(self.itunes_json.get_image(self.search_index)))
            self.itunes_name.ChangeValue(self.itunes_json.get_track_name(self.search_index))
            self.itunes_album.ChangeValue(self.itunes_json.get_album(self.search_index))
            self.itunes_genre.ChangeValue(self.itunes_json.get_genre(self.search_index))
            self.itunes_artist.ChangeValue(self.itunes_json.get_artist(self.search_index))
            track_statement = str(self.itunes_json.get_track_num(self.search_index)) + " out of " + str(self.itunes_json.get_track_cnt(self.search_index))
            self.itunes_track.ChangeValue(track_statement)
            self.itunes_year.ChangeValue("3012")
            self.Layout()
            self.Refresh()

    def on_press_search(self, event):
        value = self.text_ctrl.GetValue().replace(" ", "+")
        if value:
            self.search_index = 0
            self.itunes_json = itunesJSON(value)
            
            self.update_search()
            
        else:
            print("Type something!")

    def press_choice_left(self, event):
        self.search_index -= 1
        if self.search_index < 0:
            self.search_index = self.itunes_json.length - 1
        self.update_search()

    def press_choice_right(self, event):
        self.search_index += 1
        if self.search_index >= self.itunes_json.length:
            self.search_index =  0
        self.update_search()
    

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()