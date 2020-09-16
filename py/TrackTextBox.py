import wx
import os

class TrackTextBox:
    def __init__(self, panel, readonly=False, label=" of "):
        self.panel = panel
        self.boxer = wx.BoxSizer(wx.HORIZONTAL)
        if readonly:
            self.current_track = wx.TextCtrl(panel, style = wx.CENTER | wx.TE_READONLY, size = (50,25))
            self.album_tracks = wx.TextCtrl(panel, style = wx.CENTER | wx.TE_READONLY, size = (50,25))
        else:
            self.current_track = wx.TextCtrl(panel, style = wx.CENTER, size = (50,25))
            self.album_tracks = wx.TextCtrl(panel, style = wx.CENTER, size = (50,25))
        static = wx.StaticText(panel, style = wx.CENTER, label=label)
        self.boxer.Add(self.current_track, 0,  wx.CENTER, 5)  
        self.boxer.Add(static, 0, wx.CENTER, 5)  
        self.boxer.Add(self.album_tracks, 0, wx.CENTER, 5)
        self.current_track.SetHint('#')
        self.album_tracks.SetHint('#')

    def update(self, curr, out):
        self.current_track.ChangeValue(str(curr))
        self.album_tracks.ChangeValue(str(out))

    def getTB(self):
        return self.boxer