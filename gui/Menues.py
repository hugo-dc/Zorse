'''
Created on 09/04/2012

@author: hugo.delacruz
'''

import wx

def getMenuBar(self, window):
    window = window.upper()

    try:
        mainwindow = (('&File', 
                    (('&New', 'Create new file', self.OnNewFile),  
                     ('&Open', 'Open file', self.OnOpen),
                     ('&Save', 'Save file', self.OnSave),
                     ('Save &As...', 'Save file as...', self.OnSaveAs),
                     ('----', None, None),
                     ('&Salir', 'Abandonar Sistema', self.OnCloseMe)  
                    )
                 ),
                 ('&Ayuda', 
                     (('&Texto de ayuda', '', None),
                      ('----', None, None), 
                      ('&Acerca de...', 'Acerca de Zorse', self.OnAbout)
                     )
                 ),
                 None
                 )
    except:
        pass 

    bars = { 'MAINWINDOW': mainwindow}
    menuBar = wx.MenuBar()
    
    menues = bars[window]
    for menuset in menues:
        if menuset == None:
            break 
        
        menu_title = menuset[0]
        itemset = menuset[1]
        menu = wx.Menu()
        for item in itemset:
            item_title, item_stbar, item_handler = item
            
            if item_title == '----':
                menu.AppendSeparator()
            else:
                m_item = menu.Append(-1, item_title, item_stbar)
                if item_handler != None:
                    self.Bind(wx.EVT_MENU, item_handler, m_item)

        menuBar.Append(menu, menu_title)

    return menuBar 
