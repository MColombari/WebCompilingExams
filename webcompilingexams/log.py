from datetime import datetime
import threading


def synchronized(func):
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


class Log:
    def __init__(self, path):
        self.path = path

    @synchronized
    def write(self, row):
        with open(self.path, 'a') as f:
            date_time = datetime.today().strftime('[%Y/%m/%d') + ' - ' + datetime.now().strftime('%H:%M:%S]')
            f.write(f'\n{date_time}: ' + str(row))
