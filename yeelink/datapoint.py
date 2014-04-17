#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import json
import requests

from .utils import (UnmodifiedValue, ListValue, FloatValue, HOST, BASE_PATH,
                    timestamp_of_now)

class Datapoints(object):
    def __init__(self, apikey, device_id, sensor_id):
        self.apikey = apikey
        self.device_id = device_id
        self.sensor_id = sensor_id
        self.headers = {'U-ApiKey': self.apikey}

    def post_helper(self, data):
        """ We use this helper to post HTTP reqeust and process the HTTP
            Response

            Args:
                data, We dont care what data is, just post it

            Returns:
                True if we success to create the datapoints on yeelink platform

            Error:
                When create datapoints fail, we will raise a ValueError with
                HTTP Status Code and the error message from yeelink platform
                """
        url = ''.join([
            HOST,
            BASE_PATH,
            '/device/%s' % self.device_id,
            '/sensor/%s' % self.sensor_id,
            '/datapoints'])
        ret = requests.post(url, headers=self.headers, data=json.dumps(data))
        if ret.ok:
            return True
        raise ValueError(
                "HTTP_STATUS_CODE:%s\nERROR_MESSAGE: %s" % (
                    ret.status_code, ret.content)
                )

    def value_push(self, value, timestamp=timestamp_of_now()):
        """ To push Value Sensor Data
            Args:
                value: a num value
                timestamp: default is now, but you can assign it

            Returns:
                True if we create it successful"""

        data = {'timestamp': timestamp,
                'value': value}
        return self.post_helper(data)

    def gps_push(self, latitude, longitude, speed, offset=False,
                 timestamp=timestamp_of_now):
        """ To push GPS Sensor Data
            Args:
                latitude: latitude value
                longitude: longitude value
                speed: speed value
                offset: if you need to bias correction, pass True to this,
                        it's default to False
                timestamp: default is now, but you can assign it

            Returns:
                True if we create it successful"""

        data = {'timestamp': timestamp,
                'value': {
                    'lat': latitude,
                    'lng': longitude,
                    'speed': speed}
                }
        if offset:
            data['value'].update({'offset': 'yes'})
        return self.post_helper(data)

    def gen_push(self, value, timestamp=timestamp_of_now()):
        """ To push Gen Sensor Data
            Args:
                value: anything can be json encoded

            Returns:
                True if we create it successful"""
        data = {'timestamp': timestamp,
                'value': value}
        return self.post_helper(data)
