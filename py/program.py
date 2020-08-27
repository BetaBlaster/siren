import eyed3
import glob
import wx
import os

class DropTarget(wx.FileDropTarget): 
   def __init__(self, object): 
        wx.FileDropTarget.__init__(self) 
        self.object = object  	
   def OnDropFiles(self, x, y, data): 
        print(data[0])
        if data[0].endswith(".mp3"):
            print("CONCRETE")
            Mp3Panel.add_mp3_listing(frame.panel, data[0])
            return True 
        elif os.path.isdir(data[0]):
            print("pH of soil!!")
            Mp3Panel.update_mp3_listing(frame.panel, data[0])
            return True 
        else:
            wx.MessageBox(
                'Please drag an mp3 file here to add it or use "File>Open Folder" to add all songs in a folder',
                'Error', wx.OK | wx.ICON_ERROR
            )
            return False


class Mp3Panel(wx.Panel):    
    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.row_obj_dict = {}
        self.row_dir_dict = {}

        self.list_ctrl = wx.ListCtrl(
            self, size=(-1, 100), 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
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

        self.current_folder_path = folder_path
        self.list_ctrl.ClearAll()
        self.list_ctrl.InsertColumn(0, 'Filename', width=200)
        self.list_ctrl.InsertColumn(1, 'Song Name', width=200)
        self.list_ctrl.InsertColumn(2, 'Artist', width=140)
        self.list_ctrl.InsertColumn(3, 'Album', width=140)
        self.list_ctrl.InsertColumn(4, 'Location', width=200)
        self.row_obj_dict.clear()
        self.row_dir_dict.clear()

        mp3s = glob.glob(folder_path + '/*.mp3')
        mp3_objects = [] # USELESS?
        self.indexer = 0
        for mp3 in mp3s:
            mp3_object = eyed3.load(mp3)
            self.list_ctrl.InsertItem(self.indexer, mp3.split('/')[-1].split('.mp3')[0])
            self.list_ctrl.SetItem(self.indexer, 1, mp3_object.tag.title)
            self.list_ctrl.SetItem(self.indexer, 2, mp3_object.tag.artist)
            self.list_ctrl.SetItem(self.indexer, 3, mp3_object.tag.album)
            self.list_ctrl.SetItem(self.indexer, 4, mp3)
            mp3_objects.append(mp3_object) # USELESS
            self.row_obj_dict[self.indexer] = mp3_object
            self.row_dir_dict[self.indexer] = mp3
            self.indexer += 1
            print(self.indexer)

    def add_mp3_listing(self, file_path):

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
        print('in on_edit')


class Mp3Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, 
                          title='Mp3 Tag Editor')
        self.panel = Mp3Panel(self)
        self.create_menu()
        self.panel.update_mp3_listing(os.getcwd())
        self.Show()

    def create_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_folder_menu_item = file_menu.Append(
            wx.ID_ANY, 'Open Folder', 
            'Open a folder with MP3s'
        )
        menu_bar.Append(file_menu, '&File')
        self.Bind(
            event=wx.EVT_MENU, 
            handler=self.on_open_folder,
            source=open_folder_menu_item,
        )
        self.SetMenuBar(menu_bar)

    def on_open_folder(self, event):
        title = "Choose a directory:"
        dlg = wx.DirDialog(self, title, 
                           style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.update_mp3_listing(dlg.GetPath())
        dlg.Destroy()

if __name__ == '__main__':
    app = wx.App(False)
    frame = Mp3Frame()
    app.MainLoop()