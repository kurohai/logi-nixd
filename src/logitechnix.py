#!/usr/bin/env python


import sys
import time
import usb
import threading
import logging
from .g19_mapper import G19Mapper
from .g19_receivers import G19Receiver
from .controllers import LogitechKeyboardController
from .logutil import get_logger

log = get_logger(__name__)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


class LogitechKeyboard(object):
    """docstring for LogitechKeyboard"""

    def __init__(self, config):
        super(LogitechKeyboard, self).__init__()
        self.config = config
        self.controller = LogitechKeyboardController(
            config.vendor_id, config.device_id)

        self.__usb_device_mutex = threading.Lock()
        self.__usb_device = self.controller.usb_device
        self.__key_receiver = G19Receiver(self)
        self.__key_mapper = G19Mapper(self)
        self.__key_receiver.add_input_processor(self.__key_mapper.get_input_processor())
        self.running = True
        log.info('Logitech Keyboard Obj: {0}'.format(self))

    def start_event_handling(self):
        '''Start event processing (aka keyboard driver).

        This method is NOT thread-safe.

        '''
        # self.stop_event_handling()
        log.info('Starting event processing.')
        self.__thread_display = threading.Thread(
            target=self.__key_receiver.run)
        self.__key_receiver.start()
        self.__thread_display.start()

    def stop_event_handling(self):
        '''Stops event processing (aka keyboard driver).

        This method is NOT thread-safe.

        '''
        self.__key_receiver.stop()
        if self.__thread_display:
            self.__thread_display.join()
            self.__thread_display = None

    def read_g_and_m_keys(self, maxLen=20):
        '''Reads interrupt data from G, M and light switch keys.

        @return maxLen Maximum number of bytes to read.
        @return Read data or empty list.

        '''
        self.__usb_device_mutex.acquire()
        val = []
        try:
            val = list(self.__usb_device.handleIf1.interruptRead(
                0x83, maxLen, 10))
        except usb.USBError:
            pass
        finally:
            self.__usb_device_mutex.release()
        return val


def scan_devices(idVendor, idProduct):
    """Loop over all usb devices and try to match vendor and device ids.
    This is slow and uses more resources. The preferred way to get device
    is with get_device().
    """
    for bus in usb.busses():
        for dev in bus.devices:
            log.debug('vid: {v}\ndid: {d}'.format(
                v=hex(dev.idVendor), d=hex(dev.idProduct)))
            if hex(dev.idVendor) == idVendor and \
                    hex(dev.idProduct) == idProduct:
                return dev
    return None


class InputProcessor(object):
    """docstring for InputProcessor"""

    def __init__(self, arg):
        super(InputProcessor, self).__init__()
        self.arg = arg

    def process_input(self, input_event):
        processed = False
        if Key.G01 in inputEvent.keysDown:
            try:
                self.__virtkey.press_keycode(247)
                self.__virtkey.release_keycode(247)
            finally:
                processed = True


def get_device(vendor_id, device_id):
    """Returns device for provided vendor and device id.
    Much faster and more efficent than looping over all.
    """
    return usb.core.find(idVendor=vendor_id, idProduct=device_id)


def main():

    g510_vid = 0x46d
    g510_did = 0xc22d
    kbdev = None
    try:
        while kbdev == None:

            kbdev = get_device(g510_vid, g510_did)
            if kbdev:
                lgkb = LogitechKeyboardController(kbdev)
    except KeyboardInterrupt:
        sys.exit(0)
    log.debug(lgkb)

if __name__ == '__main__':
    main()
