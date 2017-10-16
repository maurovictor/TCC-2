## Don't forget to set up the virtualenv environment to run the code

import serial
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time
import sys
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=str, default="/dev/ttyACM0", help="define the port for serial communication")
    args = parser.parse_args()

    try:
        ser = serial.Serial()
        ser.baudrate = 9600
        ser.port = args.port
        ser.open()
        http = urllib3.PoolManager()

        while 1:
            try:
                b = ser.readline()

                real_power      = b[b.index(b'__rp__')+6: b.index(b'/__rp__')]
                apparent_power  = b[b.index(b'__ap__')+6: b.index(b'/__ap__')]
                voltage         = b[b.index(b'__vr__')+6: b.index(b'/__vr__')]
                current         = b[b.index(b'__ir__')+6: b.index(b'/__ir__')]
                power_factor    = b[b.index(b'__pf__')+6: b.index(b'/__pf__')]

                real_power2     = b[b.index(b'__rp2__')+7: b.index(b'/__rp2__')]
                apparent_power2 = b[b.index(b'__ap2__')+7: b.index(b'/__ap2__')]
                voltage2        = b[b.index(b'__vr2__')+7: b.index(b'/__vr2__')]
                current2        = b[b.index(b'__ir2__')+7: b.index(b'/__ir2__')]
                power_factor2   = b[b.index(b'__pf2__')+7: b.index(b'/__pf2__')]


                real_power3     = b[b.index(b'__rp3__')+7: b.index(b'/__rp3__')]
                apparent_power3 = b[b.index(b'__ap3__')+7: b.index(b'/__ap3__')]
                voltage3        = b[b.index(b'__vr3__')+7: b.index(b'/__vr3__')]
                current3        = b[b.index(b'__ir3__')+7: b.index(b'/__ir3__')]
                power_factor3   = b[b.index(b'__pf3__')+7: b.index(b'/__pf3__')]



                try:
                    http = urllib3.PoolManager()
                    url  = "https://emoncms.org/input/post?node=mynode&csv={0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14}&apikey=005402a13743d0838d4ecfd3b177b4aa".format(\
                                    real_power.decode('utf-8'), apparent_power.decode('utf-8'), voltage.decode('utf-8'), current.decode('utf-8'), power_factor.decode('utf-8'), \
                                    real_power2.decode('utf-8'), apparent_power2.decode('utf-8'), voltage2.decode('utf-8'), current2.decode('utf-8'), power_factor2.decode('utf-8'), \
                                    real_power3.decode('utf-8'), apparent_power3.decode('utf-8'), voltage3.decode('utf-8'), current3.decode('utf-8'), power_factor3.decode('utf-8'))
                    req = http.request('GET', url)
                    print(req.status)
                    print(url)
                except Exception as e:
                    print("Erro na requisicao")
                    print(e)
                    time.sleep(1)

            except Exception as e:
                print("-"*50)
                print()
                print("Erro ao Ler porta Serial")
                print()
                print("-"*50)
                print()
                print(e)

    except Exception as e:
        print("-"*50)
        print()
        print("Erro ao inciar a comunicação serial")
        print()
        print("-"*50)
        print()
        print(e)

if __name__ == '__main__':
    main()
