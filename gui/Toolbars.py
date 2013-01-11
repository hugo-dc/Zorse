'''
Created on 09/04/2012

@author: hugo.delacruz
'''

import wx
import Config
import Images

def getToolbar(self, toolbar, window):
	SEPARATOR = 1000
    
	mainwindow      = ""
	newconfigwindow = ""
	configwindow    = "" 

	window = window.upper()
	if window == 'MAINWINDOW':
		mainwindow = ( 
	                 ('Nuevo', 'Crear nuevo codigo fuente ABAP', Config.IMG_PATH + 'newfile.png', self.OnNewFile),
                     ('Abrir', 'Abrir archivo de codigo fuente ABAP', Config.IMG_PATH + 'fileopen.png', self.OnOpen),
 				     ('Obtener codigo fuente', 'Descarga codigo  fuente ABAP del servidor origen', Config.IMG_PATH+'download.png', self.OnDownload), 
                     ('Guardar', 'Guarda codigo en disco duro', Config.IMG_PATH + 'save.png', self.OnSave),
                     ('Comentar', 'Comenta codigo seleccionado', Config.IMG_PATH + 'comment.png', self.OnComment),
                     #('Verificar syntaxis', 'Verifica que el codigo fuente este correcto', Config.IMG_PATH + 'syntaxis.png', self.OnSyntaxis),
                     SEPARATOR,

                     ('Ejecutar codigo', 'Ejecuta codigo fuente ABAP en el servidor destino', Config.IMG_PATH+ 'execute.png', self.OnExecute),
                     #('Configurar', 'Configuracion de servidores', Config.IMG_PATH + 'configure.png', self.OnConfig),
                     SEPARATOR,
                     ('Ayuda', 'Ayuda en linea de Zorse', Config.IMG_PATH + 'help.png', self.OnHelp)
 					)
                   
	if window == 'CONFIGWINDOW':
		configwindow = ( ('Nuevo', 'Crear nueva configuracion de servidor', Config.IMG_PATH + 'new.png', self.OnNew), 
                     ('Modificar', 'Modificar configuracion de servidor', Config.IMG_PATH + 'modify.png', self.OnModify),
                     ('Eliminar', 'Eliminar configuracion de servidor', Config.IMG_PATH + 'delete.png', self.OnDelete),
                     ('Actualizar', 'Actualizar informacion', Config.IMG_PATH + 'refresh.png', None),
                      None
                     )
    
	if window == 'NEWCONFIGWINDOW':                 
		newconfigwindow = ( ('Guardar', 'Guarda configuracion', Config.IMG_PATH + 'save.png', self.OnSave), 
                            ('Probar configuracion', 'Probar configuracion', Config.IMG_PATH + 'test_config.png', self.OnTestConfig),
                     None
                    )
    
	bars = { 'MAINWINDOW': mainwindow,
             'CONFIGWINDOW': configwindow, 
             'NEWCONFIGWINDOW': newconfigwindow
            }
   
	bar = bars[window]
    
	for tool in bar:
		if tool != None:
			if tool == SEPARATOR:
				toolbar.AddSeparator()
			else:
				title, stbar, image, handler = tool
				t = toolbar.AddSimpleTool(wx.NewId(), Images.getImage(self,image), title, stbar)
				if handler != None:
					self.Bind(wx.EVT_MENU, handler, t)
	return toolbar
