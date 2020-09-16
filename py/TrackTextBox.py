import wx
import os

class TrackTextBox:
    def __init__(self, panel, label=" of "):
        self.panel = panel
        self.boxer = wx.BoxSizer(wx.HORIZONTAL)
        self.current_track = wx.TextCtrl(panel, style = wx.CENTER, size = (50,25))
        static = wx.StaticText(panel, style = wx.CENTER, label=label)
        self.album_tracks = wx.TextCtrl(panel, style = wx.CENTER, size = (50,25))
        self.boxer.Add(self.current_track, 0, wx.ALL | wx.CENTER, 5)  
        self.boxer.Add(static, 0, wx.ALL | wx.CENTER, 5)  
        self.boxer.Add(self.album_tracks, 0, wx.ALL | wx.CENTER, 5)

    def update(curr, out):
        self.current_track.ChangeValue(str(curr))
        self.album_tracks.ChangeValue(str(curr))

    def getTB(self):
        return self.boxer