from datetime import datetime

class csv_utils:
    def coalesce_date(date):
        return "" if date is None else datetime.strftime(date, '%Y-%m-%d %H:%M:%S')

    def coalesce_bool(field):
        return "" if field is None else "true" if field is True else "false"

    def coalesce_int(num):
        return "" if num is None else str(num)
