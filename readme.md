# logi-nixd #

---
## Overview ##


Custom input drivers for Logitech keyboards and others.

---
### device driver flow ###

1. init phase
    1. get logitech device by vendor and device id
    1. open device `lgkb.open()`
    1. set config 1 `lgkb.setConfiguration(1)` pass if error
    1. detach kernel driver, pass if error
    1. claim interface, error out with device in use

---
### Key Config File ###

1. yaml or json maybe, or reuse ini cfg parser
1. possibly tie into GTK or whatever to get window names for app switching.
1. 

---
## Z-Wave Game KB ##


### USB Vendor ID ###

```
Bus 008 Device 003: ID 1038:0310 SteelSeries ApS
```

