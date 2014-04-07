#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import requests

from .utils import UnmodifiedValue, ListValue, FloatValue, HOST, BASE_PATH

class Device(object):

    #we define the descriptor here
    apikey = UnmodifiedValue('apikey')
    device_id = UnmodifiedValue('device_id')
    tags = ListValue('tags')
    latitude = FloatValue('latitude')
    longitude = FloatValue('longitude')

    def __init__(self, apikey, device_id, title, about, tags, local, latitude,
                 longitude):
        self.apikey = apikey
        self.device_id = device_id
        self.title = title
        self.about = about
        self.tags = tags
        self.local = local
        self.latitude = latitude
        self.longitude = longitude
        self.headers = {'U-ApiKey': self.apikey}

    @property
    def upload_data(self):
        return {"device_id": self.device_id,
                "title": self.title,
                "about": self.about,
                "tags": self.tags,
                "location":
                    {"local": self.local,
                     "latitude": self.latitude,
                     "longitude": self.longitude
                     }
                }

    def update(self):
        url = ''.join([
            HOST,
            BASE_PATH,
            '/device',
            '/%s' % self.device_id])
        data = self.upload_data
        ret = requests.put(url, headers=self.headers, data=json.dumps(data))
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
            '/%s' % self.device_id])
        ret = requests.get(url, headers=self.headers)
        if ret.ok:
            device_info = ret.json()
            for k, v in device_info:
                #We update instance data here
                setattr(self, k, v)
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
                '/%s' % self.device_id])
        ret = requests.delete(url, headers=self.headers)
        if ret.ok:
            return True
        raise ValueError(
                "HTTP_STATUS_CODE:%s\nERROR_MESSAGE: %s" % (
                    ret.status_code, ret.content)
                )
