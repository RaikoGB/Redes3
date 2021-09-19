import time
import rrdtool
from getSNMP import consultaSNMP

while 1:
    total_input_traffic = consultaSNMP('ComunidadR3','192.168.1.70',
                     '1.3.6.1.2.1.2.2.1.11.1')
    total_output_traffic = consultaSNMP('ComunidadR3','192.168.1.70',
                     '1.3.6.1.2.1.4.3.0')

    valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
    print (valor)
    rrdtool.update('traficoRED.rrd', valor)
    rrdtool.dump('traficoRED.rrd','traficoRED.xml')
    time.sleep(1)

if ret:
    print (rrdtool.error())
    time.sleep(300)