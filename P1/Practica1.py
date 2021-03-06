from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen
import threading
import os
import rrdtool
import time
import sys
Agentes=[]
int_name=[]
int_status=[]
stop_threads = False
threads=False
Con1=0
Con2=0
Con3=0
Con4=0
Con5=0
class Agente:
    def __init__(self, ip, ver, comunidad, puerto):
         self.ip=ip
         self.ver=ver
         self.comunidad=comunidad
         self.puerto=puerto

def menu():
    print(30*"-","Menu", 30*"-")
    print("1.-Obtener bloque de ejercicios.")
    print("2.-Resumen de dispositivos monitoreados")
    print("3.-Agregar Dispositivo")
    print("4.-Eliminar Dispositivo")
    print("5.-Generar Reporte de informacion de un dispositivo")
    print("6.-Salir")

def monitor():
    interf=0
    print(30*"-","Monitor de Dispositivos", 30*"-")
    print("Agentes Monitorizados: ", len(Agentes))
    print(30*"*","Estado de conexion de los agentes", 30*"*")
    for i in Agentes:
        try:
            result = consultaSNMP(i.comunidad,
                         i.ip,
                         "1.3.6.1.2.1.1.1.0")
        except:
            print("El agente: ", i.ip ,", no se pudo conectar")
        else: 
            print("El agente: ", i.ip ," , Esta conectado") 
    print(30*"*","interfaces de Red de los agentes", 30*"*")
    #for i in Agentes:
        #R = consultaSNMP(i.comunidad,i.ip,"1.3.6.1.2.1.2.1")
    #    cmdGen = cmdgen.CommandGenerator()
    #    errorIndication, errorStatus, errorIndex, R= cmdGen.nextCmd(
    #        cmdgen.CommunityData(i.comunidad),
    #        cmdgen.UdpTransportTarget((i.ip, i.puerto)),
    #        '1.3.6.1.4.1.43.29.4.15.2.1',
    #    )
    #print(30*"=","El agente: ", i.ip, ", tiene ", R, " Interfaces", 30*"=")
    #Consulta y guarda la descripcion de las interfaces
    cmdGen = cmdgen.CommandGenerator()
    print(30*"=","Estado y descripcion de interfaces", 30*"=")
    for i in Agentes:
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, R2= cmdGen.nextCmd(
            cmdgen.CommunityData(i.comunidad),
            cmdgen.UdpTransportTarget((i.ip, i.puerto)),
            '1.3.6.1.2.1.2.2.1.2',
        )
        #R2=consultaSNMP(i.comunidad,i.ip,"1.3.6.1.2.1.2.2.1.2")
        for varBindTableRow in R2:
            for val in varBindTableRow:
                if 'Null' in val:  # Remove Null interface
                    continue
                else:
                    int_name.append(val)
        #Consulta y guarda el estado de las interfaces
        admin=''
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, R3 = cmdGen.nextCmd(
        cmdgen.CommunityData(i.comunidad),
        cmdgen.UdpTransportTarget((i.ip, i.puerto)),
        '1.3.6.1.2.1.2.2.1.7',)
        #R3 = consultaSNMP(i.comunidad,i.ip,"1.3.6.1.2.1.2.2.1.7")
        for varBindTableRow in R3:
            for val in varBindTableRow:
                admin_raw=val.prettyPrint()
                if '1' in admin_raw:
                    admin = 'UP'
                elif '2' in admin_raw:
                    admin = 'DOWN'
                elif '3' in admin_raw:
                    admin = 'TESTING'
                int_status.append(admin)
        for j in range(len(int_name)):
            print("{}\t {}\t {}".format(i.ip,int_name[j],int_status[j]))
            interf+1
        print(30*"=","El agente: ", i.ip, ", tiene ", len(int_name), " Interfaces", 30*"=")   
    input("Regresando al menu principal...")
            
def Calculo():
    print(30*"-","Obtener bloque de ejercicios.", 30*"-")
    print("Ingresa tu fecha de nacimiento")
    Dia=int(input("Dia: "))
    Mes=int(input("Mes: "))
    year=int(input("A??o: "))
    F0=date(year, Mes, Dia)
    F1=date(2021,9,10)
    Res=F1-F0
    Resultado=Res.days%3
    print("El bloque es :", Resultado)
    input("Regresando al menu principal...")

def AgregarD():
    #windows ip :192.168.1.65
    #linux ip: 192.168.1.70
    print(30*"-","Agregar un nuevo Agente", 30*"-")
    while True:        
        IP =input("Ingresa la IP del nuevo Agente: ")
        Ver=int(input("Ingresa la Version del nuevo Agente:"))
        Comunidad=input("Ingresa la Comunidad del nuevo Agente:")
        Puerto=int(input("Ingresa el puerto del nuevo Agente:"))
        Agentes.append(Agente(IP,Ver,Comunidad,Puerto))
        
        op = input("agregar Mas? (s/n): ")
        if op=="n" or op=="N":
            break
                
def BorrarD():
    print(30*"-","Eliminar un agente", 30*"-")
    IP =input("Ingresa la IP del Agente a Eliminar: ")
    for i, o in enumerate(Agentes):
        if o.ip == IP:
            del Agentes[i]
        break

def graphRRD(cont,tiempo):
    tiempo_actual = int(time.time())
    #Grafica desde el tiempo actual menos diez minutos
    tiempo_inicial = tiempo_actual - tiempo
    ret = rrdtool.graph("1.png",
                     "--start",str(tiempo_inicial),
                     "--end","N",
                     "--vertical-label=Bytes/s",
                     "--title=Paquetes de la intefaz",
                     "DEF:PackageInterface="+str(cont)+".rrd:PackageInterface:AVERAGE",
                     "AREA:PackageInterface#00FF00:Tr??fico de entrada")
    ret2 = rrdtool.graph("2.png",
                     "--start",str(tiempo_inicial),
                     "--end","N",
                     "--vertical-label=Bytes/s",
                     "--title=Recibidos IPv4",
                     "DEF:IPv4In="+str(cont)+".rrd:IPv4In:AVERAGE",
                     "LINE3:IPv4In#0000FF:Tr??fico de salida")
    ret3 = rrdtool.graph( "3.png",
                     "--start",str(tiempo_inicial),
                     "--end","N",
                     "--vertical-label=Bytes/s",
                     "--title=ICMP echoes",
                     "DEF:ICPMechoes="+str(cont)+".rrd:ICPMechoes:AVERAGE",
                     "AREA:ICPMechoes#00FF00:Tr??fico de entrada")
    ret4 = rrdtool.graph( "4.png",
                     "--start",str(tiempo_inicial),
                     "--end","N",
                     "--vertical-label=Bytes/s",
                     "--title=Segmentos Recibidoss",
                     "DEF:InSegments="+str(cont)+".rrd:InSegments:AVERAGE",
                     "LINE3:InSegments#0000FF:Tr??fico de salida")
    ret5 = rrdtool.graph( "5.png",
                     "--start",str(tiempo_inicial),
                     "--end","N",
                     "--vertical-label=Bytes/s",
                     "--title=Datagramas Entregados UDP",
                     "DEF:DatagramOut="+str(cont)+".rrd:DatagramOut:AVERAGE",
                     "AREA:DatagramOut#00FF00:Tr??fico de entrada")
        
def GenerarPDF():
    hi =A4
    print(30*"-","Menu de creacion de pdf", 30*"-")
    print("Agentes Monitorizados:")
    for i in range(len(Agentes)):
        print("ID: "+str(i)+"--IP: "+Agentes[i].ip+"--Comunidad: "+Agentes[i].comunidad)
    id=int(input("Digita el id del Agente para crear el reporte: "))
    tiempo=int(input("Digita el tiempo a graficar en segundos:"))
    for j in range(len(Agentes)):
        if j==id:
            #1.3.6.1.2.1.1.1.0 sistema operativo y sacar la img de ahi 1.3.6.1.2.1.1.6.0ese es el bueno
            #1.3.6.1.2.1.1.5.0 nombre del sistema 
            #1.3.6.1.2.1.1.6.0 ubicacion geografica?
            #1.3.6.1.2.1.1.2.0 version del sistema?seguir buscando
            #1.3.6.1.2.1.1.3.0 tiempo desde que se reinicio
            #numero de puerto
            #Comunidad
            #Ip
            Res1 = str(consultaSNMP(Agentes[j].comunidad,Agentes[j].ip,"1.3.6.1.2.1.1.1.0"))
            Res2 = str(consultaSNMP(Agentes[j].comunidad,Agentes[j].ip,"1.3.6.1.2.1.1.5.0"))
            Res3 = str(consultaSNMP(Agentes[j].comunidad,Agentes[j].ip,"1.3.6.1.2.1.1.6.0"))
            Res4 = str(consultaSNMP(Agentes[j].comunidad,Agentes[j].ip,"1.3.6.1.2.1.1.2.0"))
            Res5 = str(consultaSNMP(Agentes[j].comunidad,Agentes[j].ip,"1.3.6.1.2.1.1.3.0"))
            c = canvas.Canvas("Reporte.pdf", pagesize=A4)
            if Res1 == "Linux":
                c.drawImage("Linux.png", 20, hi-20, width=50, height=50)
            else:
                c.drawImage("Windows.png", 20, hi-20, width=50, height=50)
            text = c.beginText(50, hi-150)
            text.textLines("Nombre: "+str(Res2)+"\n"+
                           "Version: SNMP v"+str(Res4)+"\n"+
                           "SO: "+str(Res1)+"\n"+
                           "Ubicacion: "+str(Res3)+"\n"+
                           "Puertos: "+str(Agentes[j].puerto)+"\n"+
                           "Tiempo de Actividad: "+str(Res5)+"\n"+
                           "Comunidad: "+str(Agentes[j].comunidad)+"\n"+
                           "Ip: "+str(Agentes[j].ip)+"\n")
            c.drawText(text)
            graphRRD(j,tiempo)
            time.sleep(5)
            c.drawImage("1.png", 50, hi - 400, width=400, height=200)
            c.drawImage("2.png", 50, hi - 600, width=400, height=200)
            c.showPage()
            c.drawImage("3.png", 50, hi - 100, width=400, height=200)
            c.drawImage("4.png", 50, hi - 300, width=400, height=200)
            c.drawImage("5.png", 50, hi - 500, width=400, height=200)
            c.showPage()
            c.save()
        else:
            print("Agente no encontrado")

def CreateRRD():
    for i in range(len(Agentes)):
        ret = rrdtool.create(str(i)+".rrd",
                     "--start",'N',
                     "--step",'30',
                     "DS:PackageInterface:COUNTER:600:U:U",
                     "DS:IPv4In:COUNTER:600:U:U",
                     "DS:ICPMechoes:COUNTER:600:U:U",
                     "DS:InSegments:COUNTER:600:U:U",
                     "DS:DatagramOut:COUNTER:600:U:U",
                     "RRA:AVERAGE:0.5:6:5",
                     "RRA:AVERAGE:0.5:1:20")
        if ret:
            print (rrdtool.error())

def consultaSNMP(comunidad,host,oid):
    resultado=""
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado= varB.split()[2]
    return resultado

def UpdateRRD():
    x=0
    while True:
        if stop_threads==True:
            break  
        for i in range(len(Agentes)):
            x=int(i)
            #paquetes de la intefaz
            Con1= int(consultaSNMP(Agentes[i].comunidad,Agentes[i].ip,"1.3.6.1.2.1.2.2.1.11.1"))
            #Recibidos IPv4
            Con2= int(consultaSNMP(Agentes[i].comunidad,Agentes[i].ip,"1.3.6.1.2.1.4.3.0"))
            #ICMP echoes
            Con3= int(consultaSNMP(Agentes[i].comunidad,Agentes[i].ip,"1.3.6.1.2.1.5.21.0"))
            #Segmentos Recibidos
            Con4= int(consultaSNMP(Agentes[i].comunidad,Agentes[i].ip,"1.3.6.1.2.1.6.10.0"))
            #Datagramas Entregados UDP
            Con5= int(consultaSNMP(Agentes[i].comunidad,Agentes[i].ip,"1.3.6.1.2.1.7.1.0"))
            valor= "N:"+str(Con1)+":"+str(Con2)+":"+str(Con3)+":"+str(Con4)+":"+str(Con5)
            #print(valor)
            #error aqui, posiblemente modificar createRRD
            rrdtool.update(str(i)+".rdd", valor)
            rrdtool.dump(str(i)+".rdd",str(i)+".xml")
            time.sleep(1) 
    if ret:
        print (rrdtool.error())
        time.sleep(300)

while True:
    #Windows
    #os.system('cls') 
    #Linux
    os.system('clear') 
    menu()
    opcion=input("Elige una opcion: ")
    if opcion=="1":
        Calculo()
    elif opcion=="2":
        monitor()
    elif opcion=="3":
        AgregarD()
        if threads==True:
            stop_threads=True
            time.sleep(5)
            h.join()
            time.sleep(5)
            stop_threads=False
            CreateRRD()
            h = threading.Thread(target=UpdateRRD)
            h.start()
            threads=True
            
        else:
            CreateRRD()
            h = threading.Thread(target=UpdateRRD)
            h.start()
            threads=True

    elif opcion=="4":
        BorrarD()
        if threads==True:
            stop_threads=True
            time.sleep(5)
            h.join()
            time.sleep(5)
            stop_threads=False
            CreateRRD()
            h = threading.Thread(target=UpdateRRD)
            h.start()
            threads=True
        else:
            CreateRRD()
            h = threading.Thread(target=UpdateRRD)
            h.start()
            threads=True 
    elif opcion=="5":
        GenerarPDF()
    elif opcion=="6":
        if threads==True:
            stop_threads=True
            time.sleep(5)
            h.join()
            break
        else:
            break
    else:
        input("opcion invalida, intenta de nuevo...")