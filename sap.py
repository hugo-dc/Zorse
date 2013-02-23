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
    
    result = server.execute_RFC('RUN_ABAP', [program, None])
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
    abap_code = abap_code.split('\n')

    abap_h = """
REPORT ZLOAD.
constants:
    quote value ''''.
data:
	BEGIN OF T_CODE occurs 0,
		t_line(%s),
	END OF T_cODE.

"""

    abap_b = ""

    abap_f = """
INSERT REPORT '%s' FROM T_CODE.
""" % ( program.upper().strip() ) 

 
    max_l = 0
    for line in abap_code:
	    if len(line) > max_l:
		    max_l = len(line)

    abap_h = abap_h % max_l  
		
    for line in abap_code:
    	line = line.replace("'", "''")
        if len(line) > 70:
            line = line + ' '
            blocks = len(line) / 70 + 1
    	    abap_b += "T_CODE =\n'%s'\n.\n\n" % ( line[0:70] )
            abap_b += "CONCATENATE\nt_code\n"
            for i in range(1, blocks+1):
                nl = line[i*70:(i*70) + 70 ]
                nl = nl.replace("''", "'\nquote\n'")
                abap_b += "'%s'\n" % nl 
            abap_b += "INTO T_CODE. APPEND T_CODE.\n\n" 
        else:
            abap_b += "T_CODE\n = \n'%s'.\n APPEND T_CODE.\n\n" % line
    abap = abap_h + abap_b + abap_f

    abap += '\nwrite:/ sy-subrc.'
    open('code', 'w').write(abap)
    result = sap.executeABAP(abap)
    if result[0].strip() == '0':
        return True
    else:
        return False
    

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
