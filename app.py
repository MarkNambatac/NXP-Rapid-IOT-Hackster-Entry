
import pygatt
import unicodedata
import time
from Adafruit_IO import Client, Feed

adapter = pygatt.GATTToolBackend()
bluetooth_address = '00:60:37:0A:B1:4B'

#NXP Rapid IOT Characteristic UUIDS
characteristic_UUIDS = {
    "temperature": "09c0c6b0-f14c-4e4f-b94a-d3aefbfd4668",
    "humidity" :"09c0c6b0-f14c-4e4f-b94a-d3aefbfd4669",
    "air_quality_tvoc":"09c0c6b0-f14c-4e4f-b94a-d3aefbfd466a",
    "air_quality_co2": "09c0c6b0-f14c-4e4f-b94a-d3aefbfd466b",
    "pressure": "09c0c6b0-f14c-4e4f-b94a-d3aefbfd466c",
    "ambient-light": "09c0c6b0-f14c-4e4f-b94a-d3aefbfd466d"  ,
    "battery-level": "09c0c6b0-f14c-4e4f-b94a-d3aefbfd4666",
    "charging-status": "09c0c6b0-f14c-4e4f-b94a-d3aefbfd4667"
}

#Adafruit IO Configuration
ADAFRUIT_IO_USERNAME = "makoooy123"
ADAFRUIT_IO_KEY = "********************************"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

#Feeds in Adafruit IO
temp = aio.feeds('temperature')
humid = aio.feeds('humidity')
pressure = aio.feeds('pressure')
bat_status = aio.feeds('charging-status')
bat_level = aio.feeds('battery-level')
light = aio.feeds('ambient-light')


sensor_values = {}
try: 
    adapter.start()
    device = adapter.connect(bluetooth_address)
    while True:
        
        for sensor, uuid in characteristic_UUIDS.items():
            initial = device.char_read(uuid)
            value = initial.decode('utf-8').rstrip('\x00')
            sensor_values[sensor] = float(value)
        
        pressure_converted = int(str(sensor_values['pressure'])[:3])

        aio.send_data(temp.key, sensor_values['temperature'])
        aio.send_data(humid.key, sensor_values['humidity'])
        aio.send_data(pressure.key, pressure_converted)
        aio.send_data(bat_status.key, sensor_values['charging-status'])
        aio.send_data(bat_level.key, sensor_values['battery-level'])
        aio.send_data(light.key, sensor_values['ambient-light'])
        print(sensor_values)
        time.sleep(10)
    
    
finally:
    adapter.stop()

