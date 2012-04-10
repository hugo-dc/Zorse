import wx

import Toolbars
import Messages
import db
import sap

def createField(self, panel, label, size_x, y, password = False):
    wx.StaticText(panel,-1,  label, (20, y)) 
    if password: 
        text = wx.TextCtrl(panel,-1, "", pos=(120, y), size=(size_x, -1), style= wx.TE_PASSWORD)
    else:
        text = wx.TextCtrl(panel,-1, "", pos=(120, y), size=(size_x, -1))
    self.fields.append((text, label))
    return y + 25  
    
     
     
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
        
        y = createField(self, panel_left, 'ID:', 32, y)
        
        y = createField(self, panel_left, 'Nombre:', 100, y)
        y = createField(self, panel_left, 'Direccion IP:', 100, y)
        y = createField(self, panel_left, 'Numero de sistema:', 30, y)
        y = createField(self, panel_left, 'Mandante:', 32, y)
        y = createField(self, panel_left, 'Usuario:', 80, y)
        y = createField(self, panel_left, 'Password:', 80, y, True)
        
    def setParams(self):
        message = None
        self.params = []
        for field, label in self.fields:
            value = field.GetValue()
            if len(value) == 0:
                if message == None:
                    message = "Complete los siguientes campos:\n"
                label = label[:-1]
                message += label + '\n'
            else:
                self.params.append(value)
        return message
        
    def OnSave(self, event):
        message = self.setParams()
            
        if message != None:
            Messages.messageError(message, 'Guardar')
        else:
            r = db.saveServerConfig(*self.params)
            if r:
                for field, label in self.fields:
                    field.SetValue('')
        event.Skip()
        
    def OnTestConfig(self, event):
        message = self.setParams()
        if message != None:
            Messages.messageError(message, 'Probar')
        else:
            if sap.testServerConfig(*self.params):
                Messages.messageInformation('La configuracion es correcta, ahora puede guardar', 'Probar configuracion')
        event.Skip()
   