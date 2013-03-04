'''
Created on 04.03.2013

by: @hugo_dc

This window shows configured SAP Server.
You must select one in order to execute ABAP code.

'''

import wx
import db
import sap

import Toolbars
import Messages


def showSelectServer(self):
    f = SelectServer(self, id=-1, title="Select SAP Server")
    f.Show()

class SelectServer(wx.Frame):
    fields = []
    def __init__(self, parent, id, title):
        self.parent = parent
        wx.Frame.__init__(self, parent, id, title, style=wx.DEFAULT_FRAME_STYLE & ~ ( wx.RESIZE_BORDER | wx.RESIZE_BOX | wx.MINIMIZE_BOX ) , size=(250, 190) )
        
        panel = wx.Panel(self, -1)

        self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        toolbar = Toolbars.getToolbar(self, toolbar, 'selectserver')   
        toolbar.Realize()
        self.servers = db.getServers()        

        servers = []
        for server in self.servers:
            servers.append(server[0])

        wx.StaticText(panel, -1, "SAP Server: ", pos=(20, 25))
        self.choice = wx.Choice(panel, -1, pos=(120, 20), choices=servers )


    def OnExecute(self, event):
        ix = self.choice.GetCurrentSelection()

        if ix < 0:
            Messages.messageError('Select a SAP Server', 'Execute ABAP Code')
        else:
            result = sap.executeCode(self.servers[ix],  self.parent.code )
            self.parent.outtext.SetValue(result) 
        
