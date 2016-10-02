#!/usr/bin/python

import sys, time
from bluepy.btle import Peripheral

# 0x0043 register
# [0x56, red, green, blue, ???, 0xf0 for on or 0x0f for off, 0xaa]

class BleLed(Peripheral):

    SOLID_COLOR_HDL = 0x0043

    def norm_color(self, color):
        red, green, blue = color

        # normalize to 1-byte
        for c in [red, green, blue]:
            if c > 0xff:
                c = 0xff
            elif c < 0x00:
                c = 0x00

        return red, green, blue

    def set_solid_color(self, color=(0xff, 0xff, 0xff)):
        red, green, blue = self.norm_color(color)

        msg = str(bytearray([0x56, red, green, blue, 0x00, 0xf0, 0xaa]))
        self.writeCharacteristic(self.SOLID_COLOR_HDL, msg)
        self.my_color = color


    def turn_off(self):
        msg = str(bytearray([0x56, 0x00, 0x00, 0x00, 0xff, 0x0f, 0xaa]))
        self.writeCharacteristic(self.SOLID_COLOR_HDL, msg)

    def test_new(self):
        msg = str(bytearray([0xef, 0x01, 0x77]))
        self.writeCharacteristic(0x0051, str(bytearray([0x01, 0x00])))
        self.writeCharacteristic(self.SOLID_COLOR_HDL, msg)

    def fade_between(self, 
        color1=(0xff, 0xff, 0xff), color2=(0x01, 0x01, 0x01), 
        duty=0.01):
        current_color=color1
        diff_set = [1 if (y-x) > 0 else 0 for y, x in zip(color1, color2)]
        diff_set = [-1 if (y-x) < 0 else z for y, x, z in zip(color1, color2, diff_set)]
        flag = 1
        while flag:
            self.set_solid_color(current_color)
            current_color = [x-diff for x, diff in zip(current_color, diff_set)]
            
            if not any(((c1x >= ccx > c2x) or (c1x <= ccx < c2x)) for c1x, ccx, c2x in 
                zip(color1, current_color, color2)):
                diff_set = [x*-1 for x in diff_set]
                current_color = [x-diff for x, diff in zip(current_color, diff_set)]
            time.sleep(duty)

    def blink(self, color=(0xff, 0xff, 0xff), times=-1, duty=0.5):
        i = 0
        while i < times:
            self.set_solid_color(color)
            time.sleep(duty)
            self.turn_off()
            time.sleep(duty)
            i += 1

    def fade_to(self, color=(0xff, 0xff, 0xff), duty=0.1):
        diff_set = [1 if (y-x) > 0 else -1 for x, y in zip(self.my_color, color)]
        while not all(x == y for x, y in zip(self.my_color, color)):
            self.my_color = [x+y for x, y in zip(self.my_color, diff_set)]
            self.my_color = [0x01 if x < 0 else x for x in self.my_color]
            self.my_color = [0xff if x > 0xff else x for x in self.my_color]
            self.set_solid_color(self.my_color)
            time.sleep(duty)


if __name__ == "__main__":

    try:
        with open('ble_dev') as f:
            ble_dev = f.read().strip()
        light = BleLed(ble_dev)

        light.blink(times=3)
        light.set_solid_color((0x01, 0x01, 0x01))
        light.fade_to((0xff, 0xff, 0xff))

    finally:
        light.turn_off()
        light.disconnect()
