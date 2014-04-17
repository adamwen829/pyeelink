#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
from weakref import WeakKeyDictionary

HOST = "http://api.yeelink.net"
BASE_PATH = "/v1.0"

def timestamp_of_now():
    """ return a timestamp in ISO 8601 format
        example: "1991-08-29T01:02:03"""

class UnmodifiedValue(object):
    """A descripor that deny values change"""
    def __init__(self, name):
        self.name = name
        self.data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        # we get here when call instance.xxx and xxx is a UmodifiedValue ins.
        # owner is type(instance)
        return self.data[instance]

    def __set__(self, instance, value):
        # we get here when some call instance.xxx = yyy
        # xxx is a UmodifiedValue ins.
        # owner is type(instance)
        try:
            self.data[instance]
        except KeyError:
            self.data[instance] = value
            return
        raise ValueError("%s is unmodifiable." % self.name)


class ListValue(object):
    """A descripor that forbid values except list"""
    def __init__(self, name):
        self.name = name
        self.data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        # we get here when call instance.xxx and xxx is a ListValue ins.
        # owner is type(instance)
        return self.data[instance]

    def __set__(self, instance, value):
        # we get here when some call instance.xxx = yyy
        # xxx is a ListValue ins.
        # owner is type(instance)
        try:
            self.data[instance] = list(value)
        except TypeError:
            raise TypeError("%s should be a list." % self.name)

class FloatValue(object):
    """A descripor that forbid values except list"""
    def __init__(self, name):
        self.name = name
        self.data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        # we get here when call instance.xxx and xxx is a FloatValue ins.
        # owner is type(instance)
        return self.data[instance]

    def __set__(self, instance, value):
        # we get here when some call instance.xxx = yyy
        # xxx is a FloatValue ins.
        # owner is type(instance)
        try:
            self.data[instance] = float(value)
        except TypeError:
            raise TypeError("%s should be a float." % self.name)


def gen_api_url(host, base_path, path):
    return ''.join([host, base_path, path])
