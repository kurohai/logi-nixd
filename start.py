from lib import LogitechKeyboard
from lib.settings import g510


try:
    lgkb = LogitechKeyboard(g510)
except KeyboardInterrupt as e:
    sys.exit(0)

print 'logi-nixd running:', lgkb.running

lgkb.start_event_handling()

print str(lgkb.controller.keyboard)
