from datetime import datetime

class csv_utils:
    def coalesce_date( date):
        return "" if date == None else datetime.strftime(date, '%Y-%m-%d %H:%M:%S')

    def coalesce_bool( field):
        return "" if field == None else "true" if field == True else "false"

    def coalesce_int( num):
        return "" if num == None else str(num)
