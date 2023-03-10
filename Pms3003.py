import network
import machine 
import time
import gc 

class PMS:

    def __init__(self):
        self.pms = machine.UART(2,9600)
        self.pms.init(9600,bits=8,parity=None,stop=1)
        gc.enable()

    def wifi(self, ssid, pwd):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            wlan.connect(ssid,pwd)
            while not wlan.isconnected():
                pass
        print(wlan.ifconfig())


    def calc_pms(self, x,y):
        pm25 = x
        pm25 <<= 8
        pm25 = pm25 | y
        return pm25

    def extract_pms(self, raw):
        try:
            pm10=None
            pm25=None
            for i, x in enumerate(raw):
                if i+9 < len(raw)-1 and x == 66 and raw[i+1] == 77:
                    #print(raw)
                    #print(i, raw[i],raw[i+1],raw[i+6],raw[i+7],raw[i+8], raw[i+9])
                    pm25 = self.calc_pms(raw[i+6],raw[i+7])
                    pm10 = self.calc_pms(raw[i+8],raw[i+9])
                    return pm25, pm10
        except:
            pass
        return None, None


    def start(self):
        while True:
            raw = self.pms.read(42)
            pm25, pm10 = self.extract_pms(raw)    
            print(pm25, pm10)
            time.sleep(1)

if __name__ == '__main__':
    pms = PMS()
    pms.wifi("CSOffice2","")
    pms.start()
