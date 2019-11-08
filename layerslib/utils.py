from datetime import datetime
from dateutil import tz


def ts_to_dt(ts, zone='Asia/Tokyo'):
    ts = int(ts) / 1000     # msec -> sec
    utc = tz.gettz('UTC')
    tz_local = tz.gettz(zone)
    return datetime.utcfromtimestamp(int(ts)).replace(tzinfo=utc).astimezone(tz_local)
