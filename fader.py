#!/usr/bin/python

import ble_led, threading, subprocess, inspect, time

class Fader(threading.Thread):

    def __init__(self, ble_light):
        self.ble_light = ble_light
        self.method = ble_light.seven_fade
        self.args = inspect.getargspec(self.method)[3]
        self.flag = threading.Event()
        super(self.__class__, self).__init__()

    def set_duty(self, duty):
        self.ble_light.duby = duty

    def set_six_fade(self):
        self.method = ble_light.six_fade

    def set_seven_fade(self):
        self.method = ble_light.seven_fade

    def run(self):
        self.flag.clear()
        self.method(self.flag)

    def end_seq(self):
        self.flag.set()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ble_light.turn_off()
        self.ble_light.disconnect()

if __name__ == "__main__":

    try:
        with open('ble_dev') as f:
            ble_dev = f.read().strip()
        light = ble_led.BleLed(0.01, ble_dev)

        with Fader(light) as fader:
            fader = Fader(light)
            #light.seven_fade()
            print "starting..."
            fader.start()
            for i in range(5):
                time.sleep(1)
                print 5-i
            print "ending..."
            fader.end_seq()
            #wait for flag
            fader.join()

    except KeyboardInterrupt:
        fader.join()

    except Exception as e:
        print type(e)
        print e

    finally:
        pass
        #fader.ble_light.turn_off()
        #fader.ble_light.disconnect()
        