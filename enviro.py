#!/usr/bin/env python3
#
## This script gets data from the environment sensors of a Pimoroni enviro+ and
## displays them on the 0.96" Display.
## It updates the display every 30 seconds and sends the data to a InfluxDB instance.
##
## Copyright Marc Winkler - ETH Zurich - 01-07-2022

from smbus import SMBus
from bme280 import BME280
import ST7735 as display
from PIL import Image, ImageDraw, ImageFont
from enviroplus import gas
import sys
import time
import influxdbdata


# Changes these vars to your infrastructure
BGCOLOR=(0, 0, 0) #Black Background
FGCOLOR=(255,255,255) #White Foreground
FONTSIZE_TITLE=16
FONTSIZE_TEXT=13
FONTSIZE_DATA=12
FONTSIZE_GAS=14
INFLUXDB_URL="https://influxdb.phys.ethz.ch/"
INFLUXDB_USER="test"
INFLUXDB_PW="test"
INFLUXDB_DB="itl-metrics-tst"
apprentice="marc"
room="hcp_g_38-2"

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

disp = display.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)
WIDTH=disp.width
HEIGHT=disp.height

disp.begin() #This is not really needed anymore

fontTitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE_TITLE)
fontText =  ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE_TEXT)
fontData =  ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE_DATA)
fontGas =  ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE_GAS)
colour = (255,255,255)
bgimg = Image.new('RGB', (WIDTH, HEIGHT), color=BGCOLOR)
sep1 = [(49, 0), (49, 48)]
sep2 = [(106, 0), (106, 48)]
sep3 = [(0, 48), (160, 48)]
draw = ImageDraw.Draw(bgimg)
title = "Enviro:"



def print_sensor_data(sendToInflux=False):
    # We reduce the accuracy of the sensor output to zero or one digit after the
    # the comma. This does not round the number or does any kind of mathematical calc.
    temperature = float("{:.1f}".format(bme280.get_temperature()))
    humidity    = float("{:.1f}".format(bme280.get_humidity()))
    pressure    = int("{:.0f}".format(bme280.get_pressure()))
    gasData     = gas.read_all()
    gasData     = float(gasData.reducing / 1000)
    if sendToInflux:
        influxdbdata.send_data(data=temperature,measurement="temperature",apprentice=apprentice,room=room)
        influxdbdata.send_data(data=humidity,measurement="humidity",apprentice=apprentice,room=room)
        influxdbdata.send_data(data=pressure,measurement="pressure",apprentice=apprentice,room=room)
        influxdbdata.send_data(data=gasData,measurement="gas-co2",apprentice=apprentice,room=room)
    # The following lines are here to draw all the necessary things on the display.
    # It's a lot, but if you look at the comments, it all makes sense.
    # Draw a black rectangle to clear the screen, everytime before displaying new data.
    draw.rectangle((0, 0, WIDTH, HEIGHT), (0, 0, 0))
    # The next three lines draw the two vertical and one horizontal line.
    draw.line(sep1, fill = "white", width = 0)
    draw.line(sep2, fill = "white", width = 0)
    draw.line(sep3, fill = "white", width = 0)
    # The next three lines draw the (T)emperature, (H)umidity and (P)ressure letters.
    # The coordinates are always (x,y) - ([horizontal position],[vertical position])
    # The "anchor" input allows to control how the text is aligned - see: https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html?highlight=text
    draw.text((24, 2), "T", font=fontTitle, fill=colour, anchor="ma")
    draw.text((77, 2), "H", font=fontTitle, fill=colour, anchor="ma")
    draw.text((133, 2), "P", font=fontTitle, fill=colour,anchor="ma")
    # The next three lines draw the environment sensor readings and we anchor them
    # differently, to make it easier to scale.
    draw.text((24, 45), "{}C".format(temperature), font=fontData, fill=colour, anchor="md")
    draw.text((77, 45), "{}%".format(humidity), font=fontData, fill=colour, anchor="md")
    draw.text((156, 45), "{}hPa".format(pressure), font=fontData, fill=colour, anchor="rd")
    # If the CO2 Gas sensor records a reducing value equal or below 500, there is
    # too much Co2 in the air. Windows should be openened.
    if (gasData <= 500):
        gascolour="red"
    elif (gasData > 830):
        gascolour = "green"
    else:
        gascolour="white"
    draw.text((2, 62), "CO2 Gas: {:.2f} kO".format(gasData), font=fontGas, fill=gascolour, anchor="lm")
    #print(f"Gas: {gasData} kO")
    # Draw the generated image onto the display.
    disp.display(bgimg)

wait_seconds=15
try:
    while True:
        time.sleep(1)
        if wait_seconds == 0:
            print_sensor_data(sendToInflux=True)
            wait_seconds=15
        else:
            print_sensor_data()
        wait_seconds-= 1
# Turn off backlight on control-c
except KeyboardInterrupt:
    disp.set_backlight(0)
    draw.rectangle((0, 0, WIDTH, HEIGHT), (0, 0, 0))
    sys.exit(0)
except:
    disp.set_backlight(0)
    draw.rectangle((0, 0, WIDTH, HEIGHT), (0, 0, 0))
    sys.exit(0)
