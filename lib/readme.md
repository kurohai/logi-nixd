

### device driver flow ###

1. init phase
    1. get logitech device by vendor and device id
    1. open device `lgkb.open()`
    1. set config 1 `lgkb.setConfiguration(1)` pass if error
    1. detach kernel driver, pass if error
    1. claim interface, error out with device in use


### Key Config File ###

1. yaml or json maybe, or reuse ini cfg parser
1. possibly tie into GTK or whatever to get window names for app switching.
1. 
