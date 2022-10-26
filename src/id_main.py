import os

import serial
import datetime
import redis
import logging
import urllib3
import config
import request_main

cf_path = config.path['path']
cf_idcard_port = config.refrigerators['idcard']
rd = redis.StrictRedis(host='localhost', port=6379, db=0)
ser = serial.Serial(port=cf_idcard_port, baudrate=115200, timeout=1)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(filename=cf_path + 'kiosk_status.log', level=logging.DEBUG)
logger = logging.getLogger('IDS_log')
while True:
    try:
        page = rd.get('nowPage')
        log_time = datetime.datetime.now()
        log_time = log_time.strftime("%Y-%m-%d-%H:%M:%S")
        exr = datetime.datetime.now()
        exr = exr.strftime("%Y")
        exr = int(exr)
        data = ser.readline().decode('utf-8')
        if page == b'auth_adult' and len(data) > 10:
            age = int(data[4:6])
            val = str(exr - age)
            val = val[2:4]
            val = int(val)
            if val >= 19:
                logger.info(f'[{log_time} | ADULT SCAN SUCCESS : Age = {val}]')
                rd.set('msg', 'sign')
            elif val < 19:
                logger.info(f'[{log_time} | NOT ADULT : Age = {val}]')
                rd.set('msg', 'auth_fail')

    except Exception as err:
        logger.info('[ID SCANNER ERR]')
        logger.info(err)
        rd.set('msg', 'auth_fail')
