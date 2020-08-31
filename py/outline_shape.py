import wx

class RandomPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent, color):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(color)

class MasterPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent) 

        horizSplit = wx.SplitterWindow(self)
        editPaneSplit = wx.SplitterWindow(horizSplit)

        currentPanel = RandomPanel(editPaneSplit, "green")
        itunesPanel = RandomPanel(editPaneSplit, "orange")
        editPaneSplit.SplitVertically(currentPanel, itunesPanel)
        editPaneSplit.SetSashGravity(0.5)
        
        searchPanel = RandomPanel(horizSplit, "blue")
        horizSplit.SplitHorizontally(searchPanel, editPaneSplit)
        horizSplit.SetSashGravity(0.5)

        my_sizer = wx.BoxSizer(wx.VERTICAL)        
        my_sizer.Add(horizSplit, 1, wx.EXPAND)
        self.SetSizer(my_sizer)
        


class MyFrame(wx.Frame):    
    def __init__(self):
        wx.Frame.__init__(self, None, title='siren', size=(1000,700)) # sections below are size=(400,500)
        panel = MasterPanel(self)
        self.Show()



if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
