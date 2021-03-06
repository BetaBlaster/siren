import wx
import eyed3
import glob
import os
import io
import urllib.request
import json
from TrackTextBox import TrackTextBox
from itunesJSON import itunesJSON

def url_to_bmimg(img_url):
        buf = urllib.request.urlopen(img_url).read()
        sbuf = io.BytesIO(buf)
        return wx.Image(sbuf).ConvertToBitmap()

class DropTarget(wx.FileDropTarget): 
   def __init__(self, object): 
        wx.FileDropTarget.__init__(self) 
        self.object = object  	
   def OnDropFiles(self, x, y, data): 
        print(data[0])
        if data[0].endswith(".mp3"):
            frame.panel.searchPanel.add_mp3_listing(data[0])
            return True 
        elif os.path.isdir(data[0]):
            frame.panel.searchPanel.update_mp3_listing(data[0])
            return True 
        else:
            wx.MessageBox(
                'Please drag an mp3 file here to add it or use "File>Open Folder" to add all songs in a folder',
                'Error', wx.OK | wx.ICON_ERROR
            )
            return False

class SearchPanel(wx.Panel):    
    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.row_obj_dict = {}
        self.row_dir_dict = {}

        self.list_ctrl = wx.ListCtrl(self, size=(-1, 200), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'Filename', width=200)
        self.list_ctrl.InsertColumn(1, 'Song Name', width=200)
        self.list_ctrl.InsertColumn(2, 'Artist', width=140)
        self.list_ctrl.InsertColumn(3, 'Album', width=140)
        self.list_ctrl.InsertColumn(4, 'Location', width=200)
        main_sizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5)        
        edit_button = wx.Button(self, label='Edit')
        edit_button.Bind(wx.EVT_BUTTON, self.on_edit)
        main_sizer.Add(edit_button, 0, wx.ALL | wx.CENTER, 5)        
        self.SetSizer(main_sizer)

        dt = DropTarget(self.list_ctrl) 
        self.list_ctrl.SetDropTarget(dt) 

    def update_mp3_listing(self, folder_path):
        """
        Function to replace all files in mp3 listing with mp3 files in folder
        """

        self.current_folder_path = folder_path
        self.list_ctrl.ClearAll()
        self.list_ctrl.InsertColumn(0, 'Filename', width=200)
        self.list_ctrl.InsertColumn(1, 'Song Name', width=200)
        self.list_ctrl.InsertColumn(2, 'Artist', width=140)
        self.list_ctrl.InsertColumn(3, 'Album', width=140)
        self.list_ctrl.InsertColumn(4, 'Location', width=200)

        mp3s = glob.glob(folder_path + '/*.mp3')
        self.indexer = 0
        for mp3 in mp3s:
            mp3_object = eyed3.load(mp3)
            self.list_ctrl.InsertItem(self.indexer, mp3.split('/')[-1].split('.mp3')[0])
            self.list_ctrl.SetItem(self.indexer, 1, mp3_object.tag.title)
            if mp3_object.tag.artist: self.list_ctrl.SetItem(self.indexer, 2, mp3_object.tag.artist)
            if mp3_object.tag.album: self.list_ctrl.SetItem(self.indexer, 3, mp3_object.tag.album)
            self.list_ctrl.SetItem(self.indexer, 4, mp3) # Make rest of space
            self.row_obj_dict[self.indexer] = mp3_object
            self.row_dir_dict[self.indexer] = mp3
            self.indexer += 1
            print(self.indexer)

    def add_mp3_listing(self, file_path):
        """
        Function to add mp3 song to listing 
        """

        print(self.row_dir_dict.values())

        if file_path not in self.row_dir_dict.values():
            self.row_dir_dict[self.indexer] = file_path
            mp3_object = eyed3.load(file_path)
            self.row_obj_dict[self.indexer] = mp3_object
            
            self.list_ctrl.InsertItem(self.indexer, file_path.split('/')[-1].split('.mp3')[0])
            self.list_ctrl.SetItem(self.indexer, 1, mp3_object.tag.title)
            self.list_ctrl.SetItem(self.indexer, 2, mp3_object.tag.artist)
            self.list_ctrl.SetItem(self.indexer, 3, mp3_object.tag.album)
            self.list_ctrl.SetItem(self.indexer, 4, file_path)
            print(self.indexer)
            self.indexer += 1
            print(self.indexer)
        else:
            wx.MessageBox(
                'File already in list!',
                'Error', wx.OK | wx.ICON_ERROR
            )

    def on_edit(self, event):
        choice = self.list_ctrl.GetFirstSelected()
        item = self.list_ctrl.GetItem(itemIdx=choice, col=4).GetText()
        print('in on_edit')
        print(item)
        frame.panel.currentPanel.load_file(item)
        # POPULATE SEARCH FIELD aaaaand search?

class LocalFilePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        overall_sizer = wx.BoxSizer(wx.VERTICAL)

        self.missing_img = wx.Bitmap(os.getcwd() + "/missing.jpg")

        self.mp3_obj = eyed3.load(os.getcwd() + "/test.mp3")

        self.title = wx.StaticText(self, style = wx.CENTER, label="Current File Metadata:")
        overall_sizer.Add(self.title, 0, wx.ALL | wx.CENTER, 5)     

        
        self.img_bitmap = wx.StaticBitmap(self, -1, self.missing_img, (10,10));

        overall_sizer.Add(self.img_bitmap, 0, wx.ALL | wx.CENTER, 5)     
           
        fields_master = wx.BoxSizer(wx.HORIZONTAL)
        fields_left = wx.BoxSizer(wx.VERTICAL) 
        fields_right = wx.BoxSizer(wx.VERTICAL) 

        self.current_name = wx.TextCtrl(self, style = wx.TE_READONLY, size = (200,25))
        self.current_album = wx.TextCtrl(self, style = wx.TE_READONLY, size = (200,25))
        self.current_genre = wx.TextCtrl(self, style = wx.TE_READONLY, size = (200,25))
        self.current_artist = wx.TextCtrl(self, style = wx.TE_READONLY, size = (200,25))
        self.trackbox = TrackTextBox(self, True)
        self.current_track = self.trackbox.getTB()
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
        self.current_year.SetHint('Year')

        self.SetSizer(overall_sizer)

    def load_file(self, path):
        self.mp3_obj = eyed3.load(path)
        self.update_text()
        self.update_image()
    
    def update_text(self):
        if self.mp3_obj.tag.title: self.current_name.ChangeValue(self.mp3_obj.tag.title)
        if self.mp3_obj.tag.album: self.current_album.ChangeValue(self.mp3_obj.tag.album)
        if self.mp3_obj.tag.genre: self.current_genre.ChangeValue(str(self.mp3_obj.tag.genre)) #See whats up with this; maybe list of genres
        if self.mp3_obj.tag.artist: self.current_artist.ChangeValue(self.mp3_obj.tag.artist)
        if self.mp3_obj.tag.track_num: self.trackbox.update(str(self.mp3_obj.tag.track_num[0]), str(self.mp3_obj.tag.track_num[1]))
        self.current_year.ChangeValue("Will be added eventually")

    def update_image(self):
        if self.mp3_obj.tag.images:
            img = io.BytesIO(self.mp3_obj.tag.images[0].image_data)
            self.mp3_img = wx.Image(img).Scale(200, 200).ConvertToBitmap()
            self.img_bitmap.SetBitmap(self.mp3_img)
        else:
            self.img_bitmap.SetBitmap(self.missing_img)

class RandomPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent, color):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(color)

class InputPanel(wx.Panel):
        
    def __init__(self, parent):
        super().__init__(parent)
        my_sizer = wx.BoxSizer(wx.VERTICAL)      

        search_master = wx.BoxSizer(wx.VERTICAL)
        search_searcher = wx.BoxSizer(wx.HORIZONTAL)

        self.text_ctrl = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER, size = (300,25)) #add bind for pressing enter
        self.text_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_press_search)
        search_searcher.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        self.my_btn = wx.Button(self, label='Search')
        self.my_btn.Bind(wx.EVT_BUTTON, self.on_press_search)
        search_searcher.Add(self.my_btn, 0, wx.ALL | wx.CENTER, 5)   
        search_master.Add(search_searcher, 0, wx.ALL | wx.CENTER, 5)   

        ### second row of search area - left+right buttons #
        search_selection = wx.BoxSizer(wx.HORIZONTAL)
        but_left = wx.Button(self, label='left')
        but_left.Bind(wx.EVT_BUTTON, self.press_choice_left)
        search_selection.Add(but_left, 1, wx.ALL | wx.CENTER, 5)   
        self.search_index = 0
        self.json_selected = wx.StaticText(self, label="0 of 0")
        search_selection.Add(self.json_selected, 1, wx.LEFT | wx.RIGHT | wx.CENTER, 30)   
        but_right = wx.Button(self, label='right')
        but_right.Bind(wx.EVT_BUTTON, self.press_choice_right)
        search_selection.Add(but_right, 1, wx.ALL | wx.CENTER, 5) 
        search_master.Add(search_selection, 0, wx.CENTER)
        my_sizer.Add(search_master, 0, wx.ALL | wx.CENTER, 5)    


        img = url_to_bmimg("https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/b9/ab/a7/b9aba7fd-bccd-9e84-8cc6-41f616ddb429/source/200x200bb.jpg")
        self.my_img_bitmap = wx.StaticBitmap(self, -1, img, (10,10));
        my_sizer.Add(self.my_img_bitmap, 0, wx.ALL | wx.CENTER, 5) 


        fields_master = wx.BoxSizer(wx.HORIZONTAL)
        fields_left = wx.BoxSizer(wx.VERTICAL) 
        fields_right = wx.BoxSizer(wx.VERTICAL) 

        self.itunes_name = wx.TextCtrl(self, size = (200,25))
        self.itunes_album = wx.TextCtrl(self, size = (200,25))
        self.itunes_genre = wx.TextCtrl(self, size = (200,25))
        self.itunes_artist = wx.TextCtrl(self, size = (200,25))
        self.trackbox = TrackTextBox(self)
        self.itunes_track = self.trackbox.getTB() #wx.TextCtrl(panel, size = (200,25))
        self.itunes_year = wx.TextCtrl(self, size = (200,25))

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


        self.SetSizer(my_sizer)      
        my_sizer.Fit(self) 
        
    def update_search(self):

            self.json_selected.SetLabel(str(self.search_index + 1) + " out of " + str(self.itunes_json.length))
        
            self.my_img_bitmap.SetBitmap(url_to_bmimg(self.itunes_json.get_image(self.search_index)))
            self.itunes_name.ChangeValue(self.itunes_json.get_track_name(self.search_index))
            self.itunes_album.ChangeValue(self.itunes_json.get_album(self.search_index))
            self.itunes_genre.ChangeValue(self.itunes_json.get_genre(self.search_index))
            self.itunes_artist.ChangeValue(self.itunes_json.get_artist(self.search_index))
            self.trackbox.update(str(self.itunes_json.get_track_num(self.search_index)), str(self.itunes_json.get_track_cnt(self.search_index)))
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

class MasterPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent) 

        horizSplit = wx.SplitterWindow(self)
        editPaneSplit = wx.SplitterWindow(horizSplit)

        self.currentPanel = LocalFilePanel(editPaneSplit)
        self.itunesPanel = InputPanel(editPaneSplit)
        editPaneSplit.SplitVertically(self.currentPanel, self.itunesPanel)
        editPaneSplit.SetSashGravity(0.5)
        
        self.searchPanel = SearchPanel(horizSplit)
        horizSplit.SplitHorizontally(self.searchPanel, editPaneSplit)
        horizSplit.SetSashGravity(0.5)

        my_sizer = wx.BoxSizer(wx.VERTICAL)        
        my_sizer.Add(horizSplit, 1, wx.EXPAND)
        self.SetSizer(my_sizer)
        
class MainFrame(wx.Frame):    
    def __init__(self):
        wx.Frame.__init__(self, None, title='siren', size=(1000,700)) # sections below are size=(400,500)
        self.panel = MasterPanel(self)
        self.create_menu()

        self.panel.searchPanel.update_mp3_listing(os.getcwd())
        
        self.Show()


    def create_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        add_file_menu_item = file_menu.Append(wx.ID_ANY, 'Add MP3', 'Add an MP3 file')
        open_folder_menu_item = file_menu.Append(wx.ID_ANY, 'Open Folder', 'Open a folder with MP3s')
        menu_bar.Append(file_menu, '&File')
        self.Bind(event=wx.EVT_MENU, handler=self.on_add_file, source=add_file_menu_item,)
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_folder, source=open_folder_menu_item,)
        self.SetMenuBar(menu_bar)
        # About, Quit
        # Cut,Copy,Paste

    def on_open_folder(self, event):
        title = "Choose a directory:"
        dlg = wx.DirDialog(self, title, 
                           style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.searchPanel.update_mp3_listing(dlg.GetPath())
        dlg.Destroy()

    def on_add_file(self, event):
        print("do this shtuff")
        title = "Choose an MP3:"
        # CHANGE 'DIR'dialog to file and try to do MP3, if not just do check after select
        # dlg = wx.DirDialog(self, title, style=wx.DD_DEFAULT_STYLE)
        
        # if dlg.ShowModal() == wx.ID_OK:
        #     self.panel.update_mp3_listing(dlg.GetPath())
        # dlg.Destroy()


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
