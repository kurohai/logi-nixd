#!/usr/bin/env python


from src.logutil import get_logger
from src import LogitechKeyboard
from src.settings import g510
import sys

log = get_logger(__name__)

def main():
    log.info('Starting main process runner.')
    try:
        lgkb = LogitechKeyboard(g510)
    except KeyboardInterrupt as e:
        log.error(e)
        sys.exit(0)

        log.info('logi-nixd running: {0}'.format(lgkb.running))

        lgkb.start_event_handling()

        log.info(str(lgkb.controller.keyboard))


if __name__ == '__main__':
    main()
