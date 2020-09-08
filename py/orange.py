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
        self.current_itunes_name = wx.TextCtrl(panel, size = (200,25))
        self.current_tunes_artist = wx.TextCtrl(panel, size = (200,25))
        my_sizer.Add(self.current_itunes_name, 0, wx.CENTER, 20)
        my_sizer.Add(self.current_tunes_artist, 0, wx.CENTER, 20)




        panel.SetSizer(my_sizer)      
        my_sizer.Fit(self)  
        self.Show()

    def on_press(self, event):
        value = self.text_ctrl.GetValue().replace(" ", "+")
        if value:
            self.itunes_json = itunesJSON(value)
            self.my_img_bitmap.SetBitmap(url_to_bmimg(self.itunes_json.get_image()))
            self.current_itunes_name.ChangeValue(self.itunes_json.get_track_name())
            self.current_tunes_artist.ChangeValue(self.itunes_json.get_artist())
            self.Refresh()
            
        else:
            print("Type something!")

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()