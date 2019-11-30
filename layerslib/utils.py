from datetime import datetime
from dateutil import tz
import random


def ts_to_dt(ts, zone='Asia/Tokyo'):
    ts = int(ts) / 1000     # msec -> sec
    utc = tz.gettz('UTC')
    tz_local = tz.gettz(zone)
    return datetime.utcfromtimestamp(int(ts)).replace(tzinfo=utc).astimezone(tz_local)


def create_ref_id():
    # 24 chars
    d = datetime.now().strftime('%Y%m%d%H%M%S%f')
    s = ''.join([random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(4)])
    return f"{d}{s}"
