import sys
from flask import Flask, render_template, request
from ble_led import BleLed

app = Flask(__name__)

with open('ble_dev') as f:
    dev = f.read().strip()
light = BleLed(0.05, dev)

@app.route('/')
def root():
    return render_template('index.html', color="#FFFFFF")

@app.route('/solid_color', methods=['POST'])
def solid_color():
    color = request.form['color'][1:]
    rgb = [int(x, 16) for x in [color[i:i+2] for i in range(0, len(color), 2)]]
    light.set_solid_color(rgb)
    return render_template('index.html', color="#{0}".format(color))

@app.route('/turn_off', methods=['GET', 'POST'])
def turn_off():
    light.turn_off()
    return render_template('index.html', color="#FFFFFF")


if __name__ == "__main__":
    ip = '0.0.0.0'
    port = 5000
    if len(sys.argv) >= 2:
        ip = sys.argv[1]
    if len(sys.argv) == 3:
        port = sys.argv[2]
    app.run(host = ip, port=port)