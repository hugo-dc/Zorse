'''
Created on 10/04/2012

@author: hugo.delacruz
'''

import wx
import db

import Toolbars
import NewConfigurationWindow
import Messages



def showConfigWindow(self):
    f = ConfigWindow(self, id=-1, title="Configurar Servidores")
    f.Show()
    

# Config Window 
class ConfigWindow(wx.Frame):
    item = None
    selected = None
    deselected = None
    totalservers = 0
    
    def __init__(self, parent, id, title):
        #wx.Frame.__init__(self, parent, id, title, style= wx.MINIMIZE_BOX | wx.CLOSE_BOX, size=(600,300))
        wx.Frame.__init__(self, parent, id, title,   style = wx.DEFAULT_FRAME_STYLE , size=(600,300) )
        #wx.Dialog.__init__(self, parent, id, title)
        self.list = None
        
        panel1 = wx.Panel(self, -1)        
        #self.add_new = wx.BitmapButton(self, -1, wx.Bitmap(INSTALL_PATH + 'new.png'), pos=(4,10))
        #self.modify = wx.BitmapButton(self, -1, wx.Bitmap(INSTALL_PATH + 'modify.png'), pos=(4,40))
        #self.delete = wx.BitmapButton(self, -1, wx.Bitmap(INSTALL_PATH + 'delete.png'), pos=(4,70))
        #self.refresh = wx.BitmapButton(self, -1, wx.Bitmap(INSTALL_PATH + 'refresh.png'), pos=(4,100))
        
        #self.Bind(wx.EVT_BUTTON, self.OnNew, self.add_new)
        #self.Bind(wx.EVT_BUTTON, self.OnModify, self.modify)
        #self.Bind(wx.EVT_BUTTON, self.OnDelete, self.delete)
        #self.Bind(wx.EVT_BUTTON, self.OnrE, self.add_new)

        #panel2 = wx.Panel(self, -1)
        self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        toolbar = Toolbars.getToolbar(self, toolbar, 'configwindow')
        toolbar.Realize()
        
        servers = db.getServers()
        
        cols = ['ID', 'Nombre', 'Direccion Ip', 'SYSNR', 'MANDT', 'USER']
        n_col = len(cols)
        
        self.totalservers = len(db.getServers())
        
        if True:
        #if self.totalservers > 0:
            self.list = wx.ListCtrl(self, -1, size=(600,300), pos = (30, 0), style=wx.LC_REPORT)
            self.list.Show()     
            
            for x in range(n_col): #columnas
                self.list.InsertColumn(x, cols[x])
                
            
            for server in servers: #
                y = 0
                for item in server:
                    if y == 0:
                        pos = self.list.InsertStringItem(y, item)
                    else:
                        self.list.SetStringItem(pos, y, item)                    
                    y +=1
         
        if self.list != None:
            self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
            self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.list)
        
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(panel1, 1, wx.EXPAND | wx.ALL)
        #box.Add(panel2, 0, wx.EXPAND | wx.ALL)
        
    def OnItemSelected(self, event):
        self.selected = event.GetItem()
        self.sel_text = event.GetItem().GetText()
        if self.deselected != None:
            if self.sel_text == self.des_text:
                self.deselected = None
        
    def OnItemDeselected(self, event):
        self.deselected = event.GetItem()
        self.des_text = event.GetItem().GetText()
        
        if self.selected != None:
            if self.sel_text == self.des_text:
                self.selected = None        
        event.Skip()
        
        
    def OnModify(self, event):
        if self.selected == None:
            Messages.messageError('No se ha seleccionado ningun servidor', 'Modificar configuracion')
        else:
            NewConfigurationWindow.showModifWindow(self)
            
        event.Skip()
        
    def OnDelete(self, event):
        if self.selected == None:
            Messages.messageError('No se ha seleccionado ningun servidor', 'Eliminar configuracion')
        else:
            ret = Messages.messageChoice('Realmente desea eliminar la configuracion?', 'Eliminar configuracion')
            if ret == wx.ID_YES:
                if db.deleteConfig(self.sel_text):
                    self.list.DeleteItem(self.selected)
        event.Skip()
        
    def OnNew(self, event):
        NewConfigurationWindow.showNewConfigWindow(self)
        event.Skip()
        


