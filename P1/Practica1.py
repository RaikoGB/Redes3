from datetime import date
import os
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
    print("muestra monitor")
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
def AgregarD():
    pass
def BorrarD():
    pass
def GenerarPDF():
    pass
while True:
    #Windows
    os.system('cls') 
    #Linux
    #os.system('clear') 
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