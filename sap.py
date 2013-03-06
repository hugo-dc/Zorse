import easysap
    
import os    
import security


#-----------------------------------------------------------------------
# SAP
def getConnString(id, name, ip, sysnr, client, user, passwd):
    passwd = security.decode(passwd)
    return easysap.getConnString(ip, sysnr, client, user, passwd)    
    
    

def syntaxCheck(server, code):
    abap_hd = """
    REPORT ZCHECK_SYNTAX.
    
    DATA:
        comm type string value '''',
        ti_abap TYPE TABLE OF string,
        mess TYPE string,
        lin  TYPE i,
        wrd  TYPE string,
        dir  TYPE trdir,
        line type string.
    """
    
    abap_bd = ""
    l = 0
    for line in code:
        l+=1
        if len(line) == 0 or line[0] == '*':
            continue
            
        if len(line.rstrip()) == 0:
            line = ' '
        else:
            line = line.rstrip()
        
        #abap_bd += "CONCATENATE \n comm \n'"+line + "' comm INTO line."
        if line.find("'") >= 0:
            line = line.replace("'", "' comm '")
        else:
            line = line + " ' space ' "
        
        #if (len(line) + 11) > 72:
            #bunch = int(len(line)) / 72
            #i = 0
            #next = 0
            #while i < bunch:
                #next = len(line[i*72:])
                #if next > 72:
                    #next = 72
                #st = line[i*72:next]
                #if i == 0:
                    #line = "\nCONCATENATE \n '" + st + "' into line."
                #else:
                    #line = "\nCONCATENATE line \n " + st + " into line." 
                #i += 1
                
            #return 'Ancho de columna debe ser menor a 72, '+str(l)+', '+str(len(line))
        #else:
        if True:
            line = "\nCONCATENATE \n '" + line + "' into line."
        
        abap_bd += line
        
        abap_bd += "\nAPPEND line to ti_abap."
        
    abap_ft = """
        SYNTAX-CHECK FOR ti_abap 
        MESSAGE mess 
        LINE lin 
        WORD wrd 
        DIRECTORY ENTRY dir.
        
        IF SY-SUBRC = 4.
            WRITE:/ mess.
        ENDIF.
    """
    
    abap_code = abap_hd + abap_bd + abap_ft
    sc = open('syntax_check.abap', 'w')
    sc.write(abap_code)
    sc.close()
    result = executeCode(server, 'syntax_check')
    os.remove('syntax_check.abap')
    
    result.rstrip()
    if len(result) == 0:
        return None
    else:
        return result
    
    
    
    
def executeCode(server, program):
    program = program.upper()
    con_string = getConnString(*server)
    server = easysap.SAPInstance()
    server.set_config(con_string)
    
    #result = server.execute_RFC('RUN_ABAP', [program, None])
    result = server.executeABAP(program)
    retstr = ""
    for line in result:
        retstr += line + '\n'
    return retstr

def getCode(server, program):
    program = program.upper()
    con_string = getConnString(*server)
    server = easysap.SAPInstance()
    server.set_config(con_string)
    
    return server.download_abap(program)
    

def uploadCode(server, program, abap_code):
    con_string = getConnString(*server)
    sap = easysap.SAPInstance()
    sap.set_config(con_string)
    result = sap.upload_abap(program, abap_code)
    return result

def testServerConfig(id, name, ip, sysnr, client, user, passwd):
    ztest = """
    REPORT ZTEST_CONFIG.
    WRITE:/ 'IT WORKS'.
    """
    z = open('ztest.abap', 'w')
    z.write(ztest)
    z.close()
    
    server = easysap.SAPInstance()
    server.set_config('ASHOST='+ip+' SYSNR='+sysnr+' CLIENT='+client+' USER='+user+' PASSWD='+passwd)
    result = server.execute_RFC('RUN_ABAP', ['ztest', None])
    for line in result:
        if line.rstrip() == 'IT WORKS':
            return True
            break
    return False
