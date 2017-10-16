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
                real_power     = b[b.index(b'__rp__')+6: b.index(b'/__rp__')]
                apparent_power = b[b.index(b'__ap__')+6: b.index(b'/__ap__')]
                voltage        = b[b.index(b'__vr__')+6: b.index(b'/__vr__')]
                current        = b[b.index(b'__ir__')+6: b.index(b'/__ir__')]
                try:
                    http = urllib3.PoolManager()
                    url  = "https://emoncms.org/input/post?node=mynode&csv={0},{1},{2},{3}&apikey=005402a13743d0838d4ecfd3b177b4aa".format(real_power.decode('utf-8'), apparent_power.decode('utf-8'), voltage.decode('utf-8'), current.decode('utf-8'))
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
        print("-"*30)
        print()
        print("Erro ao inciar a comunicação serial")
        print()
        print("-"*30)
        print()
        print(e)

if __name__ == '__main__':
    main()
