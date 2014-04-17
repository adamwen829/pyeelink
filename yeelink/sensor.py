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

    def __init__(self, apikey, device_id, title='', about='', tags=[],
                 sensor_type='', sensor_id='', extra=None):
        self.apikey = apikey
        self.device_id = device_id
        self.sensor_id = sensor_id
        self.title = title
        self.about = about
        self.sensor_type = sensor_type
        self.tags = tags
        self.headers = {'U-ApiKey': self.apikey}
        if self.sensor_type == Sensor.VALUE_TYPE:
            self.unit_name = extra['name']
            self.unit_symbol = extra['symbol']

    @classmethod
    def all(cls, apikey='', device_id=''):
        headers = {'U-ApiKey': apikey}
        url = ''.join([
            HOST,
            BASE_PATH,
            '/device/%s' % device_id,
            '/sensors'])
        ret = requests.get(url, headers=headers)
        if ret.ok:
            sensor_list = []
            for data in ret.json():
                sensor = Sensor(
                        apikey=apikey,
                        device_id=device_id,
                        sensor_id=data['id'],
                        about=data['about'])
                sensor_list.append(sensor)
            return sensor_list
        raise ValueError(
                "HTTP_STATUS_CODE:%s\nERROR_MESSAGE: %s" % (
                    ret.status_code, ret.content))

    @property
    def data(self):
        content = {
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

    def create(self):
        url = ''.join([
                HOST,
                BASE_PATH,
                '/device',
                '/%s' % self.device_id,
                '/sensors'])
        data = dict(self.data.items() + {'type': self.sensor_type}.items())
        ret = requests.post(
                url,
                headers=self.headers,
                data=json.dumps(data))
        if ret.ok:
            self.sensor_id = ret.json()['sensor_id']
            return True
        raise ValueError(
                "HTTP_STATUS_CODE:%s\nERROR_MESSAGE: %s" % (
                    ret.status_code, ret.content)
                )

    def push(self):
        url = ''.join([
            HOST,
            BASE_PATH,
            '/device',
            '/%s' % self.device_id,
            '/sensor',
            '/%s' % self.sensor_id])
        data = json.dumps(self.data)
        ret = requests.put(url, headers=self.headers, data=data)
        if ret.ok:
            return True
        raise ValueError(
                "HTTP_STATUS_CODE:%s\nERROR_MESSAGE: %s" % (
                    ret.status_code, ret.content)
                )

    def pull(self):
        url = ''.join([
            HOST,
            BASE_PATH,
            '/device',
            '/%s' % self.device_id,
            '/sensor',
            '/%s' % self.sensor_id])
        ret = requests.get(url, headers=self.headers)
        if ret.ok:
            print ret.content
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
            '/%s' % self.device_id,
            '/sensor',
            '/%s' % self.sensor_id])
        ret = requests.delete(url, headers=self.headers)
        if ret.ok:
            return True
        raise ValueError(
                "HTTP_STATUS_CODE:%s\nERROR_MESSAGE: %s" % (
                    ret.status_code, ret.content)
                )

