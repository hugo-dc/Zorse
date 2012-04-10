import wx
    
def getImage(self, name):
    image = wx.Image(name, wx.BITMAP_TYPE_PNG)
    temp = image.ConvertToBitmap()
    return temp    
