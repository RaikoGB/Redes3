from datetime import date
from reportlab.pdfgen import *
from pysnmp.hlapi import *
from getSNMP import consultaSNMP
import threading
import os
import rrdtool
import time
Agentes=[]
int_name=[]
int_status=[]
stop_threads = False
threads=False
class Agente:
    def __init__(self, ip, ver, comunidad, puerto):
         self.ip=ip
         self.ver=ver
         self.comunidad=comunidad
         self.puerto=puerto
def UpdateRRD():
    while True:
        if stop_threads:
            break
        for i in Agente:
            #paquetes de la intefaz
            Con1= consultaSNMP(Agente[i].comunidad,Agente[i].ip,"1.3.6.1.2.1.2.2.1.11.19")
            #Recibidos IPv4
            Con2= consultaSNMP(Agente[i].comunidad,Agente[i].ip,"1.3.6.1.2.1.4.3.0")
            #ICMP echoes
            Con3= consultaSNMP(Agente[i].comunidad,Agente[i].ip,"1.3.6.1.2.1.5.21.0")
            #Segmentos Recibidos
            Con4= consultaSNMP(Agente[i].comunidad,Agente[i].ip,"1.3.6.1.2.1.6.10.0")
            #Datagramas Entregados UDP
            Con5= consultaSNMP(Agente[i].comunidad,Agente[i].ip,"1.3.6.1.2.1.7.1.0")
            valor= "N:"+str(Con1)+":"+str(Con2)+":"+str(Con3)+":"+str(Con4)+":"+str(Con5)
            #print (valor)
            rrdtool.update('traficoRED.rrd', valor)
            rrdtool.dump('traficoRED.rrd','traficoRED.xml')
            time.sleep(1)   
        if ret:
            print (rrdtool.error())
            time.sleep(300)

def menu():
    print(30*"-","Menu", 30*"-")
    print("1.-Obtener bloque de ejercicios.")
    print("2.-Resumen de dispositivos monitoreados")
    print("3.-Agregar Dispositivo")
    print("4.-Eliminar Dispositivo")
    print("5.-Generar Reporte de informacion de un dispositivo")
    print("6.-Salir")

def monitor():
    print(30*"-","Monitor de Dispositivos", 30*"-")
    print("Agentes Monitorizados: ", len(Agentes))
    print(30*"*","Estado de conexion de los agentes", 30*"*")
    for i in Agentes:
        try:
            result = netsnmp.snmpwalk("1.3.6.1.2.1.1.1",
                                      Agente[i].ver,
                                      Agente[i].ip,
                                      Agente[i].comunidad)
        except:
            print("El agente: ", Agente[i].ip ,", no se pudo conectar")
        else: 
            print("El agente: ", Agente[i].ip ," , Esta conectado") 
    print(30*"*","interfaces de Red de los agentes", 30*"*")
    for i in Agentes:
        R = consultaSNMP(Agente[i].comunidad,
                         Agente[i].ip,
                         "1.3.6.1.2.1.2.1")
        print(30*"=""El agente : ", Agente[i].ip, ", tiene ", R, " Interfaces", 30*"=")
    #Consulta y guarda la descripcion de las interfaces
    print(30*"*","Estado y descripcion de interfaces", 30*"*")
    for i in Agentes:
        R2=consultaSNMP(Agente[i].comunidad,
                         Agente[i].ip,
                         "1.3.6.1.2.1.2.2.1.2")
        for varBindTableRow in R2:
            for name, val in varBindTableRow:
                if 'Null' in val:  # Remove Null interface
                    continue
                else:
                    int_name.append(val)
    #Consulta y guarda el estado de las interfaces
        admin=''
        R3 = consultaSNMP(Agente[i].comunidad,
                         Agente[i].ip,
                         "1.3.6.1.2.1.2.2.1.7")
        for varBindTableRow in R3:
            for name, val in varBindTableRow:
                admin_raw=val.prettyPrint()
                if '1' in admin_raw:
                    admin = 'UP'
                elif '2' in admin_raw:
                    admin = 'DOWN'
                elif '3' in admin_raw:
                    admin = 'TESTING'
                int_status.append(admin)
        for j in range(len(int_name)):
            print("{}\t {}\t {}".format(Agente[i].ip,int_name[j],int_status[j]))
            
def Calculo():
    print(30*"-","Obtener bloque de ejercicios.", 30*"-")
    print("Ingresa tu fecha de nacimiento")
    Dia=int(input("Dia: "))
    Mes=int(input("Mes: "))
    year=int(input("Año: "))
    F0=date(year, Mes, Dia)
    F1=date(2021,9,10)
    Res=F1-F0
    Resultado=Res.days%3
    print("El bloque es :", Resultado)

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
        
def GenerarPDF():
    arch=canvas.Canvas("Reporte.pdf")
    arch.save()

def CreateRRD():
    ret = rrdtool.create("traficoRED.rrd",
                     "--start",'N',
                     "--step",'30',
                     "DS:inoctets:COUNTER:600:U:U",
                     "DS:outoctets:COUNTER:600:U:U",
                     "RRA:AVERAGE:0.5:6:5",
                     "RRA:AVERAGE:0.5:1:20")
    if ret:
        print (rrdtool.error())

def consultaSNMP(comunidad,host,oid):
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
            CreateRRD()
            h = threading.Thread(target=UpdateRRD)
            h.start()
        else:
            CreateRRD()
            h = threading.Thread(target=UpdateRRD)
            h.start()     
    elif opcion=="4":
        BorrarD()
        if threads==True:
            stop_threads=True
            time.sleep(5)
            h.join()
            time.sleep(5)
            CreateRRD()
            h = threading.Thread(target=UpdateRRD)
            h.start()
        else:
            CreateRRD()
            h = threading.Thread(target=UpdateRRD)
            h.start() 
    elif opcion=="5":
        GenerarPDF()
    elif opcion=="6":
        break
    else:
        input("opcion invalida, intenta de nuevo...")