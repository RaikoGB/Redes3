import time
import rrdtool
from getSNMP import consultaSNMP

while True:
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