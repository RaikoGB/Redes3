from datetime import date
import os
from pysnmp.hlapi import *
import rrdtool
Agentescc=0
Agentes=[]

class Agente:
    ver=1
    comunidad="ComunidadR3"
    puerto=161 
    def __init__(self, ip):
         self.ip=ip

def menu():
    print(30*"-","Menu", 30*"-")
    print("1.-Obtener bloque de ejercicios.")
    print("2.-Resumen de dispositivos monitoreados")
    print("3.-Agregar Dispositivo")
    print("4.-Eliminar Dispositivo")
    print("5.-Generar Reporte de informacion de un dispositivo")
    print("6.-Salir")
    pass

def monitor():
    print(30*"-","Monitor de Dispositivos", 30*"-")
    print("Agentes Monitorizados: ", Agentescc)
    print(30*"*","Estado de conexion de los agentes", 30*"*")
    i=0
    while i<=Agentescc:
        try:
            result = netsnmp.snmpwalk("1.3.6.1.4.1.9966.2.201.6.11.11",
                                      Agente[i].ver,
                                      Agente[i].ip,
                                      Agente[i].comunidad)
        except:
            print("El agente: ", Agente[i].ip ,", no se pudo conectar")
        else: 
            print("El agente: ", Agente[i].ip ," , Esta conectado") 
        i+1
    print(30*"*","interfaces de Red de los agentes", 30*"*")
    
    print(30*"*","Estado y descripcion de interfaces", 30*"*")
    pass

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
    pass

class Agente:
    ver=1
    comunidad="ComunidadR3"
    puerto=161 
    def __init__(self, ip):
         self.ip=ip

def AgregarD():
    print(30*"-","Agregar un nuevo Agente", 30*"-")
    while True:        
        IP =input("Ingresa la IP del nuevo Agente: ")
        Agentes.append(Agentescc=Agente(IP))
        Agentescc+1
        op = input("agregar Mas? (s/n): ")
        if op=="n" or op=="N":
            break
        #Al agregar un agente hacer que se inicie el update, ademas de mandar mensaje si es que se logra 
        
def BorrarD():
    print(30*"-","Eliminar un agente", 30*"-")
    #Al borrar un agente cerrar los procesos de update y reniciarlos
    IP =input("Ingresa la IP del Agente a Eliminar: ")
    for i, o in enumerate(Agentes):
        if o.ip == IP:
            del Agentes[i]
        break
        
def GenerarPDF():
    pass

def CreateRRD():
    ret = rrdtool.create("traficoRED.rrd",
                     "--start",'N',
                     "--step",'10',
                     "DS:inoctets:COUNTER:600:U:U",
                     "DS:outoctets:COUNTER:600:U:U",
                     "RRA:AVERAGE:0.5:6:5",
                     "RRA:AVERAGE:0.5:1:20")
    if ret:
        print (rrdtool.error())
    pass

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
    elif opcion=="4":
        BorrarD()
    elif opcion=="5":
        GenerarPDF()
    elif opcion=="6":
        break
    else:
        input("opcion invalida, intenta de nuevo...")