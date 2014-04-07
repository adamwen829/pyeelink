
__title__ = 'pyeelink'
__version__ = '0.0.1'
__author__ = 'Adam Wen'
__license__ = 'MIT'

from .device import Device
from .client import Client


# I copy the following code from request....
# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
