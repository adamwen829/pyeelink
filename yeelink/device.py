#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import requests

from .utils import UnmodifiedValue, ListValue, FloatValue, HOST, BASE_PATH

class Device(object):

    #we define the descriptor here
    apikey = UnmodifiedValue('apikey')

    def __init__(self, apikey, title, about, tags=[], local='', device_id='',
                 latitude='', longitude=''):
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
    def data(self):
        return {"title": self.title,
                "about": self.about,
                "tags": self.tags,
                "location":
                    {"local": self.local,
                     "latitude": self.latitude,
                     "longitude": self.longitude
                     }
                }

    @classmethod
    def all(cls, apikey=''):
        headers = {'U-ApiKey': apikey}
        url = ''.join([
                HOST,
                BASE_PATH,
                '/devices'])
        ret = requests.get(url, headers=headers)
        if ret.ok:
            device_list = []
            for data in ret.json():
                device_list.append(cls(
                    apikey=apikey,
                    device_id=data['id'],
                    title=data['title'],
                    about=data['about']))
            return device_list
        raise ValueError(
                "HTTP_STATUS_CODE:%s\nERROR_MESSAGE: %s" % (
                    ret.status_code, ret.content)
                )

    def create(self):
        url = ''.join([
                HOST,
                BASE_PATH,
                '/devices'])
        ret = requests.post(
                url,
                headers=self.headers,
                data=json.dumps(self.data))
        if ret.ok:
            self.device_id = ret.json()['device_id']
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
            '/%s' % self.device_id])
        data = self.data
        ret = requests.put(url, headers=self.headers, data=json.dumps(data))
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
            '/%s' % self.device_id])
        ret = requests.get(url, headers=self.headers)
        if ret.ok:
            device_info = ret.json()
            for k, v in device_info:
                #We update instance data here
                if k in ['local', 'latitude', 'longitude']:
                    k = ''.join(['_', k])
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
