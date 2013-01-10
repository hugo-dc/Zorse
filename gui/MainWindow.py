'''
Created on 09/04/2012

@author: hugo.delacruz
'''


import wx
import os
import webbrowser
from datetime import datetime
import sap
import Messages
import Menues
import Toolbars
import Config
import db
#import ConfigWindow
import AboutWindow

#-----------------------------------------------------------------------
#  Funciones
#-----------------------------------------------------------------------
def get_keywords():
    kw_file = open(Config.KEYWORDS_FILE, 'r').read()
    keywords = kw_file.split('\n')
    return keywords

# ARCHIVOS
def get_tmp_filename():
    fn = str(datetime.now())
    fn = 'tmp_'+fn[0:4]+fn[5:7]+fn[8:10]+fn[11:13]+fn[14:16]+fn[17:19]+'.abap'
    return fn
    

# Main Window
class MainWindow(wx.Frame):
    lastlenght = 0
    download = False
    chars = 0
    filename = None
    highlight = True
    code = None
    parameters = {}
    busy = False
    def __init__(self, parent, id, title, code = None):
        wx.Frame.__init__(self, parent, id, title,   style = wx.DEFAULT_FRAME_STYLE  )
        self.code = code            
        
        menuBar = Menues.getMenuBar(self, 'mainwindow')

        self.SetMenuBar(menuBar)
        self.statusbar = self.CreateStatusBar()
        
        #Toolbar
        toolbar = self.CreateToolBar()
        toolbar = Toolbars.getToolbar(self, toolbar, 'mainwindow')
        toolbar.Realize()
        
        self.f = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.f2 = wx.Font(12, wx.MODERN, wx.ITALIC, wx.NORMAL)
        self.f3 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD)

        #Panel
        
        panel = wx.Panel(self, -1)
        servers = []
        self.servers = db.getServers()
        
        l_pr = wx.StaticText(panel, -1, "Programa:", (15, 20))
        l_so = wx.StaticText(panel, -1, "Servidor Origen:", pos=(15, 55))

        l_sd = wx.StaticText(panel, -1, "Servidor Destino:", pos=(15, 85))

        self.t_pr  = wx.TextCtrl(panel,-1, "", pos=(100, 20),  size=(200, -1))
        self.t_pr.SetInsertionPoint(0)
        
        for server in self.servers:
            servers.append(server[0])

        self.choice1 = wx.Choice(panel, -1, pos=(120, 50), choices=servers)
        self.choice2 = wx.Choice(panel, -1, pos=(120, 80), choices=servers)

        self.codetext = wx.TextCtrl(self, -1, "",  style=wx.TE_MULTILINE|wx.TE_RICH2 | wx.TE_PROCESS_ENTER)
        self.codetext.SetInsertionPoint(0)
        
        if code != None:
            # viene un codigo por parametro
            self.codetext.SetValue(self.code)
            self.ReloadHighlight()
        
        
        panel2 = wx.Panel(self, -1)
        l_rce = wx.StaticText(panel2, -1, "Resultado:", (0, 0))
        
        self.save_result = wx.BitmapButton(panel2, -1, wx.Bitmap(Config.IMG_PATH + 'save_result.png'), pos=(0,20))
        self.Bind(wx.EVT_BUTTON, self.OnSaveResult, self.save_result)
        
        self.outtext = wx.TextCtrl(self, -1, "",style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.TE_READONLY)
        self.outtext.SetInsertionPoint(0)
        
        self.Bind(wx.EVT_TEXT, self.OnText, self.codetext)
        box2 = wx.BoxSizer(wx.VERTICAL)
        box2.Add(self.codetext, 4, wx.EXPAND | wx.ALL)
        box2.Add(panel2, 0, wx.EXPAND)
        box2.Add(self.outtext, 1, flag=wx.EXPAND)

        box = wx.BoxSizer(wx.HORIZONTAL)
        #box.Add(panel, 0, wx.EXPAND)
        box.Add(box2, 1, wx.EXPAND)
        
        self.SetSizer(box)
        
    def SyntaxHighlight(self, start, end):
        self.codetext.SetStyle(start, end, wx.TextAttr("black", "white", self.f))
        
        keywords = get_keywords()
                    
        numbers = []
        #start = 0
        #co = 0
        co = start
        
        for keyword in keywords:
            ix = self.code[start:end].upper().find(keyword.upper())
            if ix >=0:
                if ix == 0 or self.code[start+ix-1] in [' ', '\t']:
                    self.codetext.SetStyle(ix+start, ix + start + len(keyword), wx.TextAttr("orange", "white", self.f3))
                    
        for number in numbers:
            ix = self.code[start:end].find(number)
            if ix >= 0:
                self.codetext.SetStyle(ix+start, ix + start + len(number), wx.TextAttr("red", "white", self.f))
                
        stmp = start
        
        
        st = []
        
        while start < end:
            ix = self.code[start:end].find("'")
            if ix>=0:
                iy = self.code[start+ix+1:end].find("'")
                if iy>=0:
                    self.codetext.SetStyle(start+ix, start+ix+iy+2, wx.TextAttr("blue", "white", self.f))
                    start += ix + iy + 2
                    
                    st.append((stmp+ix,stmp+ix+iy+1))
                else:
                    start = end
            else:
                start = end
            
        start = stmp    
        
        ix = self.code[start:end].find('"')
        if ix>=0:
            found = False
            
            for s in st:
                if ix+start > s[0] and ix+start < s[1]:
                    found = True
                    break
                    
            if not found:
                self.codetext.SetStyle(start+ix, end, wx.TextAttr("forest green", "white", self.f2))
            
        
        if len(self.code) > start:
            if self.code[start] == '*':
                self.codetext.SetStyle(start, end, wx.TextAttr("forest green", "white", self.f2))
                
        
        
            
    def ReloadHighlight(self, s=0, e=-1):
        if e < 0:
            e = len(self.code)
            
        lines_of_code = self.code[s:e].split('\n')
        start = 0
        tot_l = 0
            
        for line in lines_of_code:
            tot_l += len(line) + 1
            self.SyntaxHighlight(start+s, s+tot_l+1)
            start = tot_l
            

    def ParametersSearch(self):
        start = 0
        while start < len(self.code):
            
            ix = self.code[start:].find('[R:')

            if ix >= 0:
                print '2', start
                iy = self.code[start:].find(']')
                #start += iy
                if iy >= 0:
                    print '3', start+ix+3, start+iy, self.code[start+ix+3:start+iy]
                    if not self.code[start+ix+3:start+iy] in self.parameters.keys():
                        self.parameters[self.code[start+ix+3:start+iy]] = ''
                        i = 0
                        for key in self.parameters.keys():
                            if i == 0:
                                pos = self.list.InsertStringItem(len(self.parameters), key)
                            else:
                                self.list.SetStringItem(pos, len(self.parameters)+i, key)
                            i +=1
                    start += ix + iy
                else:
                    break
            else:
                break
                
          
                
    def OnText(self, event):
        if self.busy == False:
            self.code = self.codetext.GetValue()
                
            ip = self.codetext.GetInsertionPoint()
            
            # TODO: Autotab
            if len(self.code) > 1:
                if self.code[ip-1] == '\n':
                    #obtenemos la linea anterior
                    pass

            if len( self.code ) > 3:
                if self.code[ip-1] == '\t' and self.code[ip-4:] == '*--\t':
                    self.code = self.code[:-1] + ('-') * 68
                    try:
                        self.codetext.SetValue(self.code)
                    except:
                        pass				
                    self.ReloadHighlight()	
                    self.codetext.SetInsertionPoint(len(self.code))
				
        
            #Syntax Highlight
            #obtenemos el inicio de la linea
            enter = str(self.codetext.GetValue())
            enter = enter[:ip]
            enter = enter[::-1]
            enter = enter.find('\n')
            if enter < 0:
                enter = 0
            else:
                enter = ip - enter
            
            if ip < len(self.code):
                ix = self.code[ip:].find('\n')
                if ix >0:
                    ip += ix 
            
            self.SyntaxHighlight(enter, ip)
            self.ParametersSearch()      

        event.Skip()
        
    def setServers(self, servers):
        self.servers = servers
        self.Refresh()

    def OnAbout(self, event):
        dlg = AboutWindow.AboutWindow(self)
        dlg.ShowModal()
        dlg.Destroy()
        
    def OnComment(self, event):
        if self.code == None or len(self.code) == 0:
            pass
        else:
        
            self.code = self.codetext.GetValue()
            start, end = self.codetext.GetSelection()
            start = int(start)
            end = int(end)
        
            bunch2 = self.code[start: end]
        
            newbunch = "*"
        
            if self.code[start-1] == '\n':
                newbunch = "*"
            else:
                newbunch  = '"'
            
            bunch2 = bunch2.split('\n')
        
            co = 0
            for bunch in bunch2:            
                if co != len(bunch2):
                    if co == len(bunch2):
                        newbunch = newbunch + bunch
                    else:
                        newbunch = newbunch + bunch + '\n' + '*'
                co +=1
            
        
            self.codetext.Replace(start, end, newbunch)
        
            self.ReloadHighlight(start, end)
        event.Skip()
        
    def OnNewFile(self, event):
        self.codetext.Clear()
        event.Skip()
        
    def OnOpen(self, event):
        self.busy = True
        dlg = wx.FileDialog(self, "Abrir archivo de codigo ABAP", os.getcwd(), style=wx.OPEN , wildcard = "ABAP Code (*.abap) | *.abap| Todos los archivos (*.*) | *.*") 
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.SetTitle("Zorse - " + self.filename)
            f = open(self.filename, 'r')
            self.code = f.read()
            self.codetext.Clear()
            self.codetext.SetValue(self.code)
            f.close()
            
            self.ReloadHighlight()
            
            
            
            self.t_pr.SetValue(r'' + self.filename)
        self.busy = False

    def OnSave(self, event):
        if self.filename == None:
            dlg = wx.FileDialog(self, "Guardar codigo ABAP", os.getcwd(), style=wx.SAVE | wx.OVERWRITE_PROMPT, wildcard = "ABAP Code (*.abap) | *.abap| Todos los archivos (*.*) | *.*") 
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetPath()
                self.SetTitle("Zorse - " + self.filename)
        else:
            f = open(self.filename, 'w')
            c = self.codetext.GetValue().split('\n')
            for line in c:
                f.write(line+'\n')
            f.close()
            self.t_pr.SetValue(r'' + self.filename)
            self.SetTitle("Zorse - " + self.filename)
            self.statusbar.SetStatusText('Archivo '+self.filename+' guardado...', 0)
            
        
        
    def OnSaveResult(self, event):
        dlg = wx.FileDialog(self, "Guardar resultado de ejecucion de codigo", os.getcwd(), style=wx.SAVE | wx.OVERWRITE_PROMPT, wildcard = "Text file (*.txt) | *.txt| CSV File (*.csv) | *.csv| Todos los archivos (*.*) | *.*") 
        if dlg.ShowModal() == wx.ID_OK:
            result_fn = dlg.GetPath()
            r = self.outtext.GetValue().split('\n')
            f = open(result_fn, 'w')
            for line in r:
                f.write(line+'\n')
            f.close()
                
        
        
    def OnDownload(self, event):
        self.filename = None
        self.busy = True
        self.busy = False
        event.Skip()
        
    def OnExecute(self, event):
        event.Skip()
        
    def OnSyntaxis(self, event):
        if len(self.servers) == 0:
            dlg = wx.MessageDialog(None,  'No se han configurado servidores. Desea configurar ahora?', "Configurar servidores",wx.YES_NO | wx.ICON_QUESTION)
            retCode = dlg.ShowModal()
            if (retCode == wx.ID_YES):
                ConfigWindow.showConfigWindow(self)
        else:
            program = self.t_pr.GetValue()
            if True:
                ix = self.choice2.GetCurrentSelection()
                
                if ix < 0:
                    Messages.messageError('Seleccione un servidor destino', 'Ejecutar codigo')
                else:
                    
                    code = self.codetext.GetValue()
                    code = code.split('\n')
                    syntax = sap.syntaxCheck(self.servers[ix], code)
                    
                    if syntax != None:
                        self.outtext.SetValue(syntax)
                        self.outtext.SetStyle(0, len(syntax), wx.TextAttr("red", "white", self.f))
                        Messages.messageError('Error en la syntaxis del codigo fuente', 'Verificacion')
                    else:
                        self.outtext.SetValue('')
                        Messages.messageInformation('No se encontraron errores de syntaxis', 'Verificacion')
        event.Skip()
        
    def OnHelp(self, event):
        webbrowser.open_new('https://github.com/hugo-dc/Zorse/wiki')
        event.Skip()
        
    def OnConfig(self, event):
        ConfigWindow.showConfigWindow(self)
        event.Skip()
        
    def OnCloseMe(self, event):
        self.Close(True)
