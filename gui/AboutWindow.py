import wx
import wx.html

# About
class AboutWindow(wx.Dialog):
    text = '''
    <html>
    <body bgcolor="#0980d2">
    <center>
    <p color = "#ffffff">
    <h1>Zorse</H1>
    <p color = "#ffffff"><b>Programmers:</b> hugo_dc</p>
    </center>
    </body>
    </html>
    '''

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'Acerca de Zorse 0.01', size=(440, 400))

        html_code = wx.html.HtmlWindow(self)

        html_code.SetPage(self.text)
        button = wx.Button(self, wx.ID_OK, "Aceptar")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html_code, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()