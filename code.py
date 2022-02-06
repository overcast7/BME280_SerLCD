#!/usr/bin/env python3
import time
from datetime import datetime
from influxdb import InfluxDBClient
from adafruit_bme280 import basic as adafruit_bme280
import qwiic_serlcd
import board
import busio
dbhost = "HOST ADDRESS"
dbport = "DB PORT"
dbuser = "DB USERNAME"
dbpassword = "DB PASSWORD"
dbname = "DBNAME"
port = 1

lcd = qwiic_serlcd.QwiicSerlcd(address=0x72)
lcd.begin()
lcd.leftToRight()
lcd.noCursor()

addresses = [0x76, 0x77]

client = InfluxDBClient(dbhost, dbport, dbuser, dbpassword, dbname)
timestamp = datetime.now()

for address in addresses:
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address)

    bme280.sea_level_pressure = 1033.50
    
    print(bme280.temperature)
    print(bme280.relative_humidity)
    print(bme280.pressure)

    json_body = [
            {
                "measurement": "BME280-" + hex(address),
                "tags": {
                    "host": "HOST ADDRESS",
                    "Sensor": "Sensor BME280-" + hex(address)
                },
                "Zeit": timestamp,
                "fields": {
                    "Temperatur": bme280.temperature,
                    "Luftdruck": bme280.pressure,
                    "Luftfeuchtigkeit": bme280.relative_humidity,
                }
            }
        ]

    client.write_points(json_body)

    lcd.clearScreen() 
    lcd.setFastBacklight(255, 255, 255)
    lcd.setCursor(0, 0)
    lcd.print(f"Temperatur:   {bme280.temperature} C")
    lcd.setCursor(0, 1)
    lcd.print(f"Feuchtigkeit: {bme280.relative_humidity} %")
    lcd.setCursor(0, 2)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    lcd.print(f"Uhrzeit:      {current_time}")
    time.sleep(5)
