#!/usr/bin/env python


import sys
import usb
import logging
# log = logging.getLogger('')


class LogitechKeyboardController(object):
    """docstring for LogitechKeyboardController"""

    def __init__(self, vendor_id, device_id):
        super(LogitechKeyboardController, self).__init__()
        self.vendor_id = vendor_id
        self.device_id = device_id
        self.usb_device = self.get_usb_device()
        self.keyboard = self.usb_device.open()
        try:
            self.keyboard.setConfiguration(1)
            log.debug('usb config set')
        except usb.USBError:
            pass

        try:
            self.keyboard.detachKernelDriver(1)
        except usb.USBError:
            pass

        try:
            self.keyboard.claimInterface(1)
            print('keyboard connected!')

        except usb.USBError as e:
            print "Device is in use."
            print e
            sys.exit(0)

    def get_usb_device(self):
        """Returns device for provided vendor and device id.
        Much faster and more efficent than looping over all.
        """

        dev = None
        while dev == None:
            # dev = usb.core.find(idVendor=0x46d, idProduct=0xc22d)
            # dev = usb.core.find(idVendor=self.vendor_id.encode('hex'), idProduct=self.device_id.encode('hex'))
            dev = self._scan_devices(self.vendor_id, self.device_id)
        return dev

    def __repr__(self):
        return str(self.usb_device)

    def _scan_devices(self, idVendor, idProduct):
        """Loop over all usb devices and try to match vendor and device ids.
        This is slow and uses more resources. The preferred way to get device
        is with get_device().
        """
        for bus in usb.busses():
            for dev in bus.devices:
                if hex(dev.idVendor) == idVendor and \
                        hex(dev.idProduct) == idProduct:
                    return dev
        return None
