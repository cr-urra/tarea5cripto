import imaplib
import re
import subprocess

usar = ""
while(True):
    usar = input("Desea renovar la metadata? (y: si, n: no): ")
    if usar == "y":
        #datos
        host = 'imap.gmail.com'
        imap = imaplib.IMAP4_SSL(host)

        imap.login('cr.urra6@gmail.com', 'lavidanoesloqueunopiensa')
        imap.select('Inbox')
        mails = []
        mails.append('noreply@redditmail.com')
        mails.append('newsletter@em.pedidosya.com')
        mails.append('newsletter@peta.cl')
        mails.append('newsletter@investingmail.com') 
        mails.append('envios=tpnet.es@crlsrv.com')


        def sub(x, st):
            for i in range(0, len(x)):
                if x[i] == st:
                    return i

        def messageId (x):
            x = x.replace("Message-ID:", "")
            x = x.replace(">", "")
            x = x.replace("<", "")
            x = x.replace("Message-Id:", "")
            x = x.strip()
            return x

        def getFrom (x):
            x = x.replace("From: ", "")
            x = x.strip()
            init = sub(x,'<')
            end = sub(x,'>')
            y = x[init+1:end]
            return x, y

        def getReceivedAndTime (x):
            x = x.strip()
            x = re.split("\s", x)
            indice = len(x)-1
            lines = []
            for i in range(len(x)-1, -1,-1):
                if x[i] == 'Received:':
                    lines.append(x[i:indice])
                    indice = i
            receives = []
            tim = ''
            if len(lines) >= 2:
                for i in range(0,len(lines)):
                    receives.append([])
                    for j in range(0,len(lines[i])):
                        if lines[i][j] != '':
                            if len(receives[i]) == 0:
                                receives[i] = str(lines[i][j])+" "
                            else:
                                receives[i] = str(receives[i])+str(lines[i][j])+" "
                        if i == len(receives)-1:
                            tim = lines[i][j-2]+" "+lines[i][j-1]
                    lines[i][len(lines[i])-1] = ''
            else:
                print("error")
                return None
            res = []
            if len(receives) == 2:
                res.append(receives[0].replace('Received: ',""))
                res.append(receives[1].replace('Received: ',""))
                return res,tim
            elif len(receives) >= 3:
                res.append(receives[0].replace('Received: ',""))
                res.append(receives[len(receives)-2].replace('Received: ',""))
                return res, tim

        def compare(x, y):
            for i in range(0,len(y)):
                if y[i] == x:
                    return False
            return True

        corr = [[],[],[],[],[]]
        formato = []

        '''

        # Usar solo para determinar el formato de fechas

        for i in range(0,len(mails)):
            typ, data = imap.search(None,'FROM', mails[i])
            for num in data[0].split():
                typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (Date)])')
                datito = data[0][1].decode()
                formato.append(datito)
                break
            if i == 0:
                formato[i] = formato[i][11:22] # Cortar los índices según el formato de la fecha
            else:
                formato[i] = formato[i][11:22]
            print(formato[i])

        '''

        for i in range(0,len(mails)):
            typ, data = imap.search(None,'FROM', mails[i])
            fileA = open("metaData/correo"+str(i+1)+"/messageId", "w")
            fileB = open("metaData/correo"+str(i+1)+"/from", "w")
            fileC = open("metaData/correo"+str(i+1)+"/correo", "w")
            fileD = open("metaData/correo"+str(i+1)+"/primerReceived", "w")
            fileE = open("metaData/correo"+str(i+1)+"/penultimoReceived", "w")
            fileF = open("metaData/correo"+str(i+1)+"/time", "w")
            for num in data[0].split():
                typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (Date)])')
                datito = data[0][1].decode()
                if i == 0:
                    datito = datito[11:22]
                else:
                    datito = datito[11:22]
                boolean = compare(datito, corr[i])
                print(datito)
                if(boolean):
                    corr[i].append(datito)
                    typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
                    datito = data[0][1].decode()
                    datito = messageId(datito)
                    print("Message-ID: " + datito)
                    fileA.writelines(datito+'\n')
                    typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (From)])')
                    datito = data[0][1].decode()
                    datito, aux = getFrom(datito)
                    print("From: " + datito)
                    fileB.writelines(datito+'\n')
                    print("Correo: " + aux)
                    fileC.writelines(aux+'\n')
                    typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (Received)])')
                    datito = data[0][1].decode()
                    datito, aux = getReceivedAndTime(datito)
                    for h in range(0, len(datito)):
                        print("Received: " + datito[h])
                    fileD.writelines(datito[0]+'\n')
                    fileE.writelines(datito[1]+'\n')
                    fileF.writelines(aux+'\n')
                    print("Time: "+aux)
                    print("-----------------------------")
            fileA.close()
            fileB.close()
            fileC.close()
            fileD.close()
            fileE.close()
            fileF.close()
        imap.close()
    elif usar == "n":
        break
    else:
        print("inserte entrada valida")

while(True):
    usar = input("Desea generar los regex? (y: si, n: no): ")
    if usar == "y":
        bashCommand = []
        for i in range(0,5):
            bashCommand.append([])
            bashCommand[i].append("./correo"+str(i+1)+"correo")
            bashCommand[i].append("./correo"+str(i+1)+"firstR")
            bashCommand[i].append("./correo"+str(i+1)+"from")
            bashCommand[i].append("./correo"+str(i+1)+"messageid")
            bashCommand[i].append("./correo"+str(i+1)+"penR")
            bashCommand[i].append("./correo"+str(i+1)+"time")
        for i in range(0,len(bashCommand)):
            for j in range(0, len(bashCommand[i])):
                file = ""
                if j == 0:
                    file = open("metaData/correo"+str(i+1)+"/regexCorreo", "w")
                elif j == 1:
                    file = open("metaData/correo"+str(i+1)+"/regexFirstRecieved", "w")
                elif j == 2:
                    file = open("metaData/correo"+str(i+1)+"/regexFrom", "w")
                elif j == 3:
                    file = open("metaData/correo"+str(i+1)+"/regexMessageId", "w")
                elif j == 4:
                    file = open("metaData/correo"+str(i+1)+"/regexPenultimoRecieved", "w")
                elif j == 5:
                    file = open("metaData/correo"+str(i+1)+"/regexTime", "w")
                process = subprocess.Popen(bashCommand[i][j].split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
                file.writelines(output.decode('utf-8'))
                file.close()
    elif usar == "n":
        break
    else:
        print("inserte entrada valida")
    
