from datetime import datetime, timezone
from scd4x import SCD4X
from icp10125 import ICP10125
from sgp30 import SGP30
import time
import pulsar
import logging
import sys
import subprocess
import os
import traceback
import math
import base64
import json
from time import gmtime, strftime
import random, string
import time
import psutil
import uuid
from time import sleep
from math import isnan
from subprocess import PIPE, Popen
import socket
from pulsar.schema import *
from pulsar.schema import AvroSchema
from pulsar.schema import JsonSchema
from pulsar import Client, AuthenticationOauth2
import argparse
import os.path
import re
import sys
import os

### Schema Object
# https://pulsar.apache.org/docs/en/client-libraries-python/

class thermalext(Record):
    uuid = String(required=True)
    ipaddress = String(required=True)
    cputempf = Integer(required=True)
    runtime = Integer(required=True)
    host = String(required=True)
    hostname = String(required=True)
    macaddress = String(required=True)
    endtime = String(required=True)
    te = String(required=True)
    cpu = Float(required=True)
    diskusage = String(required=True)
    memory = Float(required=True)
    rowid = String(required=True)
    systemtime = String(required=True)
    ts = Integer(required=True)
    starttime = String(required=True)
    datetimestamp = String(required=True)
    temperature = Float(required=True)
    humidity = Float(required=True)
    co2 =  Float(required=True)
    totalvocppb = Float(required=True)
    equivalentco2ppm = Float(required=True)
    pressure = Float(required=True)
    temperatureicp = Float(required=True)

# IP Address
def IP_address():
        try:
            s = socket.socket(socket_family, socket.SOCK_DGRAM)
            s.connect(external_IP_and_port)
            answer = s.getsockname()
            s.close()
            return answer[0] if answer else None
        except socket.error:
            return None

# Get MAC address of a local interfaces
def psutil_iface(iface):
    # type: (str) -> Optional[str]
    import psutil
    nics = psutil.net_if_addrs()
    if iface in nics:
        nic = nics[iface]
        for i in nic:
            if i.family == psutil.AF_LINK:
                return i.address
# Random Word
def randomword(length):
 return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()) for i in range(length))

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

#parse arguments
parse = argparse.ArgumentParser(prog='cloudsensors.py')
parse.add_argument('-su', '--service-url', dest='service_url', type=str, required=True,
                   help='The pulsar service you want to connect to')
parse.add_argument('-t', '--topic', dest='topic', type=str, required=True,
                   help='The topic you want to produce to')
parse.add_argument('--auth-params', dest='auth_params', type=str, default="",
                   help='The auth params which you need to configure the client')
args = parse.parse_args()

external_IP_and_port = ('198.41.0.4', 53)  # a.root-servers.net
socket_family = socket.AF_INET
# Timer
packet_size=3000

# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
factor = 2.25

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
ipaddress = IP_address()

print(args.service_url)
print(args.topic)
print(args.auth_params)
# connect to pulsar
if (len(args.auth_params) == 0 ):
   client = pulsar.Client(args.service_url)
else:
   client = pulsar.Client(args.service_url, authentication=AuthenticationOauth2(args.auth_params))

producer = client.create_producer(topic=args.topic ,schema=JsonSchema(thermalext),properties={"producer-name": "thermalext-py-sensor","producer-id": "thermal-sensor" })

try:
    device = SCD4X(quiet=False)
    device.start_periodic_measurement()

    sgp30 = SGP30()
    sgp30.start_measurement()

    deviceicp = ICP10125()

    while True:
        currenttime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        starttime = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        start = time.time()

        # Create unique id
        uniqueid = 'thrml_{0}_{1}'.format(randomword(3),strftime("%Y%m%d%H%M%S",gmtime()))
        uuid2 = '{0}_{1}'.format(strftime("%Y%m%d%H%M%S",gmtime()),uuid.uuid4())

        # CPU Temp
        f = open("/sys/devices/virtual/thermal/thermal_zone0/temp","r")
        cputemp = str( f.readline() )
        cputemp = cputemp.replace('\n','')
        cputemp = cputemp.strip()
        cputemp = str(round(float(cputemp)) / 1000)
        cputempf = str(round(9.0/5.0 * float(cputemp) + 32))
        f.close()

        usage = psutil.disk_usage("/")
        end = time.time()

        co2, temperature, relative_humidity, timestamp = device.measure()
        dateTimeStamp = datetime.fromtimestamp(timestamp, timezone.utc)

        result = sgp30.get_air_quality()
        pressure, temperatureicp = deviceicp.measure()
        thermalRec = thermalext()
        thermalRec.uuid = uniqueid
        thermalRec.ipaddress = ipaddress
        thermalRec.cputempf = int(cputempf)
        thermalRec.runtime =  int(round(end - start))
        thermalRec.host = os.uname()[1]
        thermalRec.hostname = host_name
        thermalRec.macaddress = psutil_iface('wlan0')
        thermalRec.endtime = '{0}'.format( str(end ))
        thermalRec.te = '{0}'.format(str(end-start))
        thermalRec.cpu = psutil.cpu_percent(interval=1)
        thermalRec.diskusage = "{:.1f} MB".format(float(usage.free) / 1024 / 1024)
        thermalRec.memory = psutil.virtual_memory().percent
        thermalRec.rowid = str(uuid2)
        thermalRec.systemtime = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        thermalRec.ts =  int( time.time() )
        thermalRec.starttime = str(starttime)

        thermalRec.datetimestamp = str(dateTimeStamp)
        thermalRec.temperature = round(float(temperature),4)
        thermalRec.humidity = round(float(relative_humidity),2)
        thermalRec.co2 =  round(float(co2),2)

        thermalRec.equivalentco2ppm = round(float(result.equivalent_co2),5)
        thermalRec.totalvocppb = round(float(result.total_voc),3)
        thermalRec.pressure = round(pressure,2)

        icptempf = (round(9.0/5.0 * float(temperatureicp) + 32))

        thermalRec.temperatureicp = round(float(icptempf),2)

        print(thermalRec)
        producer.send(thermalRec,partition_key=uniqueid)

except KeyboardInterrupt:
    pass

client.close()
