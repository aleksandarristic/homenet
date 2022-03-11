import re

dt_fmts = {
    r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}': '%Y-%m-%d %H:%M:%S',
    r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}': '%Y-%m-%d %H:%M',
    r'\d{4}-\d{2}-\d{2}': '%Y-%m-%d',
    r'\d{2}:\d{2}': '%H:%M',
    r'\d{2}:\d{2}:\d{2}': '%H:%M:%S'
}


def get_dt_format(datetime_string):
    if datetime_string is None:
        return None
    for dt_re, dt_fmt in dt_fmts.items():
        if re.match(dt_re, datetime_string):
            return dt_fmt
    return None

