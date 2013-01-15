import wx

import Toolbars
import Messages
import db
import sap
import Utils

    
     
def showModifWindow(self):
    f = NewConfigurationWindow(self, id=-1, title="Modificar configuracion")
    f.Show()
    
def showNewConfigWindow(self):
    f = NewConfigurationWindow(self, id=-1, title="Nueva configuracion")
    f.Show()    
         

class NewConfigurationWindow(wx.Frame):
    fields = []
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(300,300))
        #wx.Dialog.__init__(self, parent, id, title)
        
        panel_left = wx.Panel(self, -1)
        self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        toolbar = Toolbars.getToolbar(self, toolbar, 'newconfigwindow')
        toolbar.Realize()
        
        y = 20
        
        y = Utils.createField(self, panel_left, 'ID:', 32, y)
        
        y = Utils.createField(self, panel_left, 'Nombre:', 100, y)
        y = Utils.createField(self, panel_left, 'Direccion IP:', 100, y)
        y = Utils.createField(self, panel_left, 'Numero de sistema:', 30, y)
        y = Utils.createField(self, panel_left, 'Mandante:', 32, y)
        y = Utils.createField(self, panel_left, 'Usuario:', 80, y)
        y = Utils.createField(self, panel_left, 'Password:', 80, y, True)
        
       
    def OnSave(self, event):
        message = Utils.setParams(self)
            
        if message != None:
            Messages.messageError(message, 'Guardar')
        else:
            r = db.saveServerConfig(*self.params)
            if r:
                for field, label in self.fields:
                    field.SetValue('')
        event.Skip()
        
    def OnTestConfig(self, event):
        message = Utils.setParams(self)
        if message != None:
            Messages.messageError(message, 'Probar')
        else:
            if sap.testServerConfig(*self.params):
                Messages.messageInformation('La configuracion es correcta, ahora puede guardar', 'Probar configuracion')
        event.Skip()
   
