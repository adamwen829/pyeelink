#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import urllib

import requests

from .device import Device
from .utils import HOST, BASE_PATH, UnmodifiedValue



APIKEY = '/user/apikey?username=%s&pass=%s'

class InvalidAccount(Exception):
    pass


class WrongReqMethd(Exception):
    pass


class Client(object):
    apikey = UnmodifiedValue('apikey')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.apikey = self._exchange_for_apikey()
        self.headers = {'U-ApiKey': self.apikey}

    def _exchange_for_apikey(self):
        username = urllib.quote(self.username)
        password = urllib.quote(self.password)
        url = ''.join([
                HOST,
                BASE_PATH,
                APIKEY % (username, password)])
        ret = requests.get(url).json()
        if ret['apikey']:
            return ret['apikey']
        raise ValueError(
                "ErrorCode: %s\nErrorMessage:%s" % (
                    ret['errcode'],
                    ret['errmsg'])
                )

    def create_device(self, title, about, tags, local, latitude, longitude):
        url = ''.join([
                HOST,
                BASE_PATH,
                '/devices'])
        data = {'title': title,
                'about': about,
                'tags': tags,
                'location': {
                    'local': local,
                    'latitude': latitude,
                    'longitude': longitude}
                }
        ret = requests.post(url, headers=self.headers, data=json.dumps(data))
        if ret.ok:
            device_id = ret.json()['device_id']
            return Device(
                    apikey=self.apikey,
                    device_id=device_id,
                    title=title,
                    about=about,
                    tags=tags,
                    local=local,
                    latitude=latitude,
                    longitude=longitude)
        raise ValueError(
                "HTTP_STATUS_CODE:%s\nERROR_MESSAGE: %s" % (
                    ret.status_code, ret.content)
                )
