#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

import requests

from .utils import BASE_PATH, HOST, ListValue, UnmodifiedValue



class Sensor(object):
    # the sensor type of yeelink
    VALUE_TYPE = 'value'
    GPS_TYPE = 'gps'
    GEN_TYPE = 'gen'
    PHOTO_TYPE = 'photo'

    apikey = UnmodifiedValue('apikey')
    device = UnmodifiedValue('device')
    sensor_id = UnmodifiedValue('sensor_id')
    sensor_type = UnmodifiedValue('sensor_type')
    tags = ListValue('tags')

    def __init__(self, apikey, device, sensor_id, sensor_type, title, tags,
                 extra=None):
        self.apikey = apikey
        self.device = device
        sensor_id = sensor_id
        self.sensor_type = title
        self.tags = tags
        self.headers = {'U-ApiKey': self.apikey}
        if self.sensor_type == Sensor.VALUE_TYPE:
            self.unit_name = extra['name']
            self.unit_symbol = extra['symbol']

    @property
    def contents(self):
        content = {
                'device_id': self.device_id,
                'sensor_id': self.sensor_id,
                'type': self.sensor_type,
                'title': self.title,
                'about': self.about,
                'tags': self.tags}
        if self.sensor_type == Sensor.VALUE_TYPE:
            content.update(
                    {'unit':
                        {'name': self.unit_name,
                         'symbol': self.unit_symbol
                        }
                    })
        return content

    def update(self):
        url = ''.join([
            HOST,
            BASE_PATH,
            '/device',
            '/%s' % self.device.device_id,
            '/sensor',
            '/%s' % self.sensor_id])
        data = json.dumps(self.contents)
        ret = requests.put(url, headers=self.headers, data=data)
        if ret.ok:
            return True
        raise ValueError(
                "HTTP_STATUS_CODE:%s\nERROR_MESSAGE: %s" % (
                    ret.status_code, ret.content)
                )

    def refresh(self):
        url = ''.join([
            HOST,
            BASE_PATH,
            '/device',
            '/%s' % self.device.device_id,
            '/sensor',
            '/%s' % self.sensor_id])
        ret = requests.get(url, headers=self.headers)
        if ret.ok:
            #TODO: update instance here
            return True
        raise ValueError(
                "HTTP_STATUS_CODE:%s\nERROR_MESSAGE: %s" % (
                    ret.status_code, ret.content)
                )

    def delete(self):
        url = ''.join([
            HOST,
            BASE_PATH,
            '/device',
            '/%s' % self.device.device_id,
            '/sensor',
            '/%s' % self.sensor_id])
        ret = requests.delete(url, headers=self.headers)
        if ret.ok:
            return True
        raise ValueError(
                "HTTP_STATUS_CODE:%s\nERROR_MESSAGE: %s" % (
                    ret.status_code, ret.content)
                )

