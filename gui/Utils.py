import wx

def createField(self, panel, label, size_x, y, password = False):
    wx.StaticText(panel,-1,  label, (20, y)) 
    if password: 
        text = wx.TextCtrl(panel,-1, "", pos=(120, y), size=(size_x, -1), style= wx.TE_PASSWORD)
    else:
        text = wx.TextCtrl(panel,-1, "", pos=(120, y), size=(size_x, -1))
    self.fields.append((text, label))
    return y + 25  
    
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
 
