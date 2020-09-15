import wx
import os

class TrackTextBox(wx.BoxSizer):
    def __init__(self, panel):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL) 
        self.panel = panel
        boxer = wx.BoxSizer(wx.HORIZONTAL)
        self.current_track = wx.TextCtrl(panel, style = wx.CENTER, size = (50,25))
        static = wx.StaticText(panel, style = wx.CENTER, label=" of ")
        self.album_tracks = wx.TextCtrl(panel, style = wx.CENTER, size = (50,25))
        boxer.Add(self.current_track, 0, wx.ALL | wx.CENTER, 5)  
        boxer.Add(static, 0, wx.ALL | wx.CENTER, 5)  
        boxer.Add(self.album_tracks, 0, wx.ALL | wx.CENTER, 5)

    def update(curr, out):
        self.current_track.ChangeValue(str(curr))
        self.album_tracks.ChangeValue(str(curr))