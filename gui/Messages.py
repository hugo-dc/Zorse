import wx

#-------------------------------------------------------------------------
def messageChoice(message, title):
    dlg = wx.MessageDialog(None, message, title, wx.YES_NO | wx.ICON_WARNING)
    res = dlg.ShowModal()
    return res

def messageInformation(message, title):
    dlg = wx.MessageDialog(None, message, title, wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()

def messageError(message, title):
    dlg = wx.MessageDialog(None, message, title, wx.OK | wx.ICON_ERROR)
    dlg.ShowModal()
