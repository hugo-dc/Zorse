# -*- coding: ISO-8859-1 -*-
import wx
import gui.Messages
import sys, traceback
import os
import gui.MainWindow
import gui.Config

reload(sys)
sys.setdefaultencoding( "latin-1" )



#------------------------------------------------------------------------------------------------
# Ventanas
#------------------------------------------------------------------------------------------------
# Progress
class ExecutionProgress(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Ejecutando codigo...', size=(350,150))
        panel = wx.Panel(self, -1)
        self.count = 0
        self.gauge = wx.Gauge(panel, -1, 50, (20,50), (250, 25))
        self.gauge.SetBezelFace(3)
        self.gauge.SetShadowWidth(3)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        
    def OnIdle(self, event):
        self.count = self.count + 1.
        if self.count >= 50:
            self.count = 0
        self.gauge.SetValue(self.count)
        
    
class Zorse(wx.App):
    fname = 'Untitled'
    code  = None
    def init(self, fname = None, code = None):
        self.fname = fname
        self.code = code 
        print code
        
    def OnInit(self):
        # Opening logo window
        image = wx.Image(gui.Config.IMG_PATH + 'splash.png', wx.BITMAP_TYPE_PNG)
        image = image.ConvertToBitmap()
        
        wx.SplashScreen(image, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 1500, None, -1)
        wx.Yield()
        
        
        fname = 'Zorse - ' + self.fname
        self.frame = gui.MainWindow.MainWindow(parent=None, id=-1, title=fname, code =code)
        self.frame.Maximize()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        
        return True
        
    def OnExit(self):
        pass


if __name__ == '__main__':
    name = 'Untitled'
    code = None
    if len(sys.argv) > 1:
        in_fi = sys.argv[1]
        if os.path.exists(in_fi):
            in_file = open(in_fi, 'r')
            code = in_file.read()
            in_file.close()
            fname = in_fi			
    try:
        App = Zorse(name, code)
        App.MainLoop()
    except:
        traceback.print_exc(file=open('exceptions', 'w'))
        error = open('exceptions', 'r').read()
        gui.Messages.messageError('Se ha detectado un error, considere enviar un email con la impresion de pantalla a la direccion: hugo.delacruz@mazlibre.com\n\n '+error, 'Zorse')
        os.remove('exceptions')
    
