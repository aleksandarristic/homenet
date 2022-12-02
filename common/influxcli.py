from influxdb import InfluxDBClient
from django.conf import settings

DB_ADDRESS = settings.INFLUXDB_CONFIG['DB_ADDRESS']
DB_PORT = settings.INFLUXDB_CONFIG['DB_PORT']
DB_USER = settings.INFLUXDB_CONFIG['DB_USER']
DB_PASSWORD = settings.INFLUXDB_CONFIG['DB_PASSWORD']
DB_DATABASE = settings.INFLUXDB_CONFIG['DB_DATABASE']


class Cli(object):
    def __init__(self):
        self.c = InfluxDBClient(DB_ADDRESS, DB_PORT, DB_USER, DB_PASSWORD, DB_DATABASE)

    def get_speedtest(self):
        result_set = self.c.query('SELECT LAST(*) FROM speedtest')
        return result_set.get_points().__next__()

cli = Cli()
