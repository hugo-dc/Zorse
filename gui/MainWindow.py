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
import ConfigWindow
import AboutWindow
import Download
import SelectServer
import random


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
    download   = False
    chars      = 0
    filename   = None
    highlight  = True
    code       = None
    parameters = {}
    busy       = False
    local      = False

    def __init__(self, parent, id, title, code = None):
        wx.Frame.__init__(self, parent, id, title,   style = wx.DEFAULT_FRAME_STYLE  )
        self.code = code            
        self.saved = True 
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
        self.panel = wx.Panel(self, -1)
        self.panel.SetBackgroundColour("aquamarine")

        # Navigation
        self.CreateTree("New Project")
        
        tree = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

        self.codetext = wx.TextCtrl(self, -1, "",  style=wx.TE_MULTILINE|wx.TE_RICH2 | wx.TE_PROCESS_ENTER | wx.HSCROLL)
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
        box.Add(self.panel, 0, wx.EXPAND)
        box.Add(box2, 1, wx.EXPAND)
        
        self.SetSizer(box)

        self.lastpath = os.getcwd()

        self.servers = db.getServers()
        self.local = True

    def CreateTree(self, name):
        il = wx.ImageList(16,16)

        self.fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))
        self.fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16, 16)))
        self.fileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_OTHER, (16, 16)))

        self.tree = wx.TreeCtrl(self.panel, size=(250, 100), style=wx.TR_DEFAULT_STYLE )
        self.tree.SetBackgroundColour("cadet blue")

        treeSizer = wx.BoxSizer(wx.VERTICAL)
        treeSizer.Add(self.tree, 1, wx.EXPAND)
        self.panel.SetSizer(treeSizer)

        self.tree.AssignImageList(il)
 
        root = self.tree.AddRoot(name)
        self.tree.SetItemImage(root, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(root, self.fldropenidx, wx.TreeItemIcon_Expanded)
        self.tree.SetItemPyData(root, None)

    def ChangeRootName(self, name, force = False):
        root = self.tree.GetRootItem()
        line = ""
        start = 0

        if not force:
            while line == "":
                first_nl = self.code[start].find('\n')
                line = self.code[start:first_nl]
                line = line.strip()
                words = line.split()
                if words[0] == 'REPORT':
                    name = words[1].replace('.', '').upper()
                if words[0] == 'FUNCTION':
                    name = words[1].replace('.', '').upper()
                if words[0] == 'INCLUDE':
                    name = words[1].replace('.', '').upper()
                start = first_nl    

        self.tree.SetItemText(root, name)

    def AddTreeNodes(self, parentItem, items):
        for item in items:
            if type(item) == str:
                newItem = self.tree.AppendItem(parentItem, item)
                self.tree.SetItemPyData(newItem, None)
                self.tree.SetItemImage(newItem, self.fileidx, wx.TreeItemIcon_Normal)
            else:
                newItem = self.tree.AppendItem(parentItem, item[0])
                self.tree.SetItemPyData(newItem, None)
                self.tree.SetItemImage(newItem, self.fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(newItem, self.fldropenidx, wx.TreeItemIcon_Expanded)

                self.AddTreeNodes(newItem, item[1])

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
                    self.codetext.SetStyle(ix+start, ix + start + len(keyword), wx.TextAttr("blue", "white", self.f3))
                    
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
                    self.codetext.SetStyle(start+ix, start+ix+iy+2, wx.TextAttr("blue violet", "white", self.f))
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
        if not self.busy: 
            self.busy = True
            if e < 0:
                e = len(self.code)
            
            lines_of_code = self.code[s:e].split('\n')
            start = 0
            tot_l = 0
            
            for line in lines_of_code:
                tot_l += len(line) + 1
                self.SyntaxHighlight(start+s, s+tot_l+1)
                start = tot_l
            self.busy = False    
                
    def OnText(self, event):
        if self.busy == False:
            if self.saved:
                self.SetTitle(self.GetTitle()+'[+]')
            self.code = self.codetext.GetValue()
            self.saved = False
                
            ip = self.codetext.GetInsertionPoint()
            
            # TODO: Autotab
                
            if len( self.code ) >= 4:
                #if self.code[ip-1] == '-'  and self.code[ip-4:] == '\n*--':
                   
                if self.code[ip-1] == '\t' and ( self.code[ip-5:] == '\n*--\t' or len(self.code) == 4 ):
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
            #self.ParametersSearch()      

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
        if not self.saved:
            res = Messages.messageChoice("Archivo no ha sido guardado, Desea guardar?", 'Archivo sin guardar')
            if res == wx.ID_OK:
                OnSave(self, event)
        self.codetext.Clear()
        self.filename = None
        self.tree.SetBackgroundColour('cadet blue')
        self.SetTitle('Zorse - Untitled')
        event.Skip()
        
    def OnOpen(self, event):
        self.busy = True
        self.local = True
        
        dlg = wx.FileDialog(self, "Abrir archivo de codigo ABAP", self.lastpath, style=wx.OPEN , wildcard = "ABAP Code (*.abap) | *.abap| Todos los archivos (*.*) | *.*") 
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.SetTitle("Zorse - " + self.filename)
            f = open(self.filename, 'r')
            self.code = f.read()
            self.codetext.Clear()
            self.codetext.SetValue(self.code)
            f.close()
            self.busy = False            
            self.ReloadHighlight()
            #self.t_pr.SetValue(r'' + self.filename)
            #self.CreateTree(self.filename)
            self.local = True
            self.ChangeRootName(self.filename)
        self.busy = False

    def OnSaveAs(self, event):
        event.skip()

    def OnSave(self, event):
        if self.filename == None:
            dlg = wx.FileDialog(self, "Guardar codigo ABAP", os.getcwd(), style=wx.SAVE | wx.OVERWRITE_PROMPT, wildcard = "ABAP Code (*.abap) | *.abap| Todos los archivos (*.*) | *.*") 
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetPath()
                self.SetTitle("Zorse - " + self.filename)
                self.saved = True
            else: 
                return
        
        f = open(self.filename, 'w')
        c = self.codetext.GetValue().split('\n')
        for line in c:
            f.write(line+'\n')
        f.close()
        self.SetTitle("Zorse - " + self.filename)
        self.statusbar.SetStatusText('Archivo '+self.filename+' guardado...', 0)
        self.saved = True
        self.ReloadHighlight()
            
        
        
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
        if len(self.servers) == 0:
            rc = Messages.messageChoice("SAP Server configuration not found. Do you want to configure?", "Server configuration")
            if rc == wx.ID_YES :
                ConfigWindow.showConfigWindow(self)

        else:        
            Download.Show(self)
        self.busy = False
        event.Skip()
        
    def OnUpload(self, event):
        if self.local:
            Messages.messageError('This is not an SAP source code', 'Cannot upload current source code')
        else:
            if self.sap_program.strip()[0].lower() not in 'xyz':
                Messages.messageError('This seems a standard ABAP code!', 'Not a chance!')
            else:    
                result = sap.uploadCode(self.sap_server, self.sap_program, self.code)            
                if result:
                    Messages.messageInformation('ABAP Code uploaded to SAP Server successfully', 'Upload')
                else:
                    Messages.messageError('An error occured while uploading ABAP Code', 'ERROR')

    def OnExecute(self, event):
        SelectServer.showSelectServer(self)
        event.Skip()
        
    def OnSyntaxis(self, event):
        if len(self.servers) == 0:
            dlg = wx.MessageDialog(None,  'No se han configurado servidores. Desea configurar ahora?', "Configurar servidores",wx.YES_NO | wx.ICON_QUESTION)
            retCode = dlg.ShowModal()
            if (retCode == wx.ID_YES):
                ConfigWindow.showConfigWindow(self)
        else:
            #program = self.t_pr.GetValue()
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
