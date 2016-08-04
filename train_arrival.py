import urllib2, json, pdb, time, datetime

from ble_led import BleLed

stop = "239N"
blinks = 3
DEBUG = True

# open up the ble device
with open('ble_dev') as f:
    dev = f.read().strip()
lamp = BleLed(dev)

lamp.set_solid_color((0x01, 0x01, 0x01))

while True:

    res = urllib2.urlopen("http://trains.bcpearce.com/stop/{0}".format(stop))

    arrivals = json.loads(res.read())
    print "Scanned arrivals @ {0}".format(datetime.datetime.now())
    if DEBUG:
        for a in arrivals:
            print a

    if any(((x[0] == '2' or x[0] == '3') and x[1] < 0 and x[1] > -60) for x in arrivals):
        for _ in range(blinks):
            lamp.set_solid_color((0xff, 0x00, 0x00))
            time.sleep(1)
            lamp.set_solid_color((0x01, 0x00, 0x00))
            time.sleep(1)

    if any(((x[0] == '4' or x[0] == '5' or x[0] == '5X') and x[1] < 0 and x[1] > -60) for x in arrivals):
        for _ in range(blinks):
            lamp.set_solid_color((0x00, 0xff, 0x00))
            time.sleep(1)
            lamp.set_solid_color((0x00, 0x01, 0x00))
            time.sleep(1)

    time.sleep(30)