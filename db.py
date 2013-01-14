import os
import sqlite3
import sap
import gui.Messages
import security
import wx
# BASE DE DATOS
  
INSTALL_PATH = os.getcwd()
INSTALL_PATH = INSTALL_PATH.replace('\\\\', '/')
INSTALL_PATH = INSTALL_PATH.replace('\\', '/') + '/'


def executeQuery(query, q = 'S', val=True):
    r = None
    if val:
        createDatabase()
            
    con = sqlite3.connect(INSTALL_PATH + 'cfg.dll')
    cur = con.cursor()
    cur.execute(query) 
    if q == 'S':
        r = cur.fetchall()
    if q == 'I':
        r = con.commit()
    cur.close()
    con.close()
    return r

def createDatabase():
    if not os.path.exists(INSTALL_PATH + 'cfg.dll'): 
        query = """ CREATE TABLE Servers(id TEXT, name TEXT, ip TEXT, sysnr TEXT, client TEXT, user TEXT, passwd TEXT, PRIMARY KEY(id)) """
        executeQuery(query, 'I', False)

        query = "CTREATE TABLE Config(id TEXT, lastpath TEXT, PRIMARY KEY(id) )"
        executeQuery(query, 'I', False)
        
        #query = """ CREATE TABLE Images(id text, name text, 

def getServers():
    #if existDatabase():
    servers_data = executeQuery(""" SELECT * FROM Servers """)
    servers = []
    for server in servers_data:
        servers.append(server)
    return servers
    
def cypher(text):
    return text
    
def keyExists(id):
    query = "SELECT * FROM Servers WHERE id = '"+id+"'"
    r = executeQuery(query)
    if len(r) >0:
        return True
    else:
        return False
    

    
    
def saveServerConfig(id, name, ip, sysnr, client, user, passwd):
    if not keyExists(id): 
        #?????
        save = True
        if sap.testServerConfig(id, name, ip, sysnr, client, user, passwd):
            save = True
        else:
            ret = gui.Messages.messageChoice('No se pudo conectar al servidor, aun asi desea guardar la configuracion?', 'Guardar')
            if ret == wx.ID_YES:
                save = True
            else:
                save = False
        
        if save:
            passwd = security.encode(passwd)
            query = "INSERT INTO Servers VALUES('"+id+"', '"+name+"', '" + ip + "', '"+ sysnr + "', '"+client + "', '"+user+"', '"+passwd+"')"
            executeQuery(query, q='I')
            if keyExists(id):
                gui.Messages.messageInformation('El registro se ha guardado con exito', 'Guardar configuracion de servidor')
                return True
            else:
                gui.Messages.messageError('Ocurrio un error desconocido, la configuracion no pudo guardarse', 'Guardar configuracion de servidor')
                return False
        
    else:
        gui.Messages.messageError('El ID ya existe!', 'Guardar configuracion de servidor')
        return False
        
def deleteConfig(id):
    query = "DELETE FROM Servers WHERE id = '"+id+"'"
    executeQuery(query, q='I')
    if keyExists(id):
        gui.Messages.messageError('Error: No se elimino el registro!', 'Eliminando configuracion')
        return False
    else:
        gui.Messages.messageInformation('El registro se elimino correctamente', 'Eliminando configuracion')
        return False
    
