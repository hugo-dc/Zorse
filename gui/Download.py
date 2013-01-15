# 14.01.2013
# @hugo_dc

# Download code from SAP Server

import wx
import Toolbars
import Utils
import sap 
import Messages
import db

def Show(self):
    f = DownloadCode(self, id=-1, title="Download ABAP Sourcecode")
    f.Show()

class DownloadCode(wx.Frame):
    fields = []
    def __init__(self, parent, id, title):
        self.parent = parent
        wx.Frame.__init__(self, parent, id, title, style = wx.DEFAULT_FRAME_STYLE, size=(250, 190) )
        panel = wx.Panel(self, -1)

        self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        toolbar = Toolbars.getToolbar(self, toolbar, 'downloadwindow')
        toolbar.Realize()
        self.fields = []
        self.servers = db.getServers()

        servers = []
        for server in self.servers:
            servers.append(server[0])
        
        wx.StaticText(panel, -1, "SAP Server: ", pos=(20, 55))
        self.choice = wx.Choice(panel, -1, pos=(120, 50), choices=servers )


        y = 20

        y = Utils.createField(self, panel, 'Program name:', 100, y)

    def OnDownload(self, event):
        message = Utils.setParams(self)
        if message != None:
            Messages.messageError(message, 'Error downloading code')
        else:
            ix = self.choice.GetCurrentSelection()

            if ix < 0:
                Messages.messageError('Select a server', 'Download ABAP Source code')
            else:    
                abap = sap.getCode(self.servers[ix], self.params[0])
                if abap != "":
                    self.parent.code = abap
                    self.parent.codetext.SetValue(abap)
                    self.parent.ReloadHighlight()
                    Messages.messageInformation('Source Code downloaded successfully!', 'Download')
                    self.parent.local = False
                    self.parent.ChangeRootName(self.params[0].upper(), True)
                    self.parent.sap_program = self.params[0].upper()
                    self.parent.sap_server  = self.servers[ix]
                    self.parent.tree.SetBackgroundColour('blue violet')
                    self.Destroy()
                else:
                    Messages.messageError('Error downloading program', 'Error downloading code')               
        
