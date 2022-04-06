from datetime import datetime

from django.db import models, transaction


class BaseTestModel(models.Model):
    objects = models.Manager()

    server = models.CharField('Server Name', max_length=100, null=True, default=None)

    created = models.DateTimeField("Created on", auto_now_add=True)
    updated = models.DateTimeField("Updated on", auto_now=True)
    entry_type = models.CharField(max_length=20, default="TEST")

    success = models.BooleanField(default=False)

    start_time = models.DateTimeField("Start time")
    test_date = models.DateField("Test date")
    duration = models.FloatField('Duration (s)', default=0)
    data = models.TextField(null=True, default=None)

    class Meta:
        abstract = True
        ordering = ['-start_time']


class SpeedTest(BaseTestModel):
    is_average = models.BooleanField(default=False)
    running = models.BooleanField(default=False)

    server_id = models.PositiveSmallIntegerField('Server ID', null=True, default=None)
    latency = models.FloatField("Latency", null=True, default=None)
    jitter = models.FloatField("Jitter", null=True, default=None)
    download = models.PositiveIntegerField("Download speed", default=0)
    upload = models.PositiveIntegerField("Upload speed", default=0)
    dl_bytes = models.PositiveBigIntegerField("Downloaded bytes", default=0)
    ul_bytes = models.PositiveBigIntegerField("Uploaded bytes", default=0)
    share_url = models.CharField("Share URL", max_length=100, null=True, default=None)

    def __str__(self):
        return f'Speedtest(time={self.start_time}, success={self.success}, dl={self.download}, ul={self.upload}, ' \
               f'lat={self.latency})'

    @classmethod
    def start(cls, start_time, data=None, server_id=None):
        obj = cls(
            server_id=server_id,
            start_time=start_time,
            running=True,
            success=True,  # hackity hack
            is_average=False,
            data=data,
            test_date=datetime.date(start_time),
            entry_type='SPEED'
        )
        obj.save()
        transaction.commit()
        return obj

    def stop(self, server=None, success=False, server_id=None, latency=None, jitter=None, download=0, upload=0, dl_bytes=0, ul_bytes=0,
             share_url=None, data=None, duration=None):

        self.running = False
        self.server = server or self.server
        self.success = success
        self.server_id = server_id or self.server_id
        self.latency = latency or self.latency
        self.jitter = jitter or self.jitter
        self.download = download or self.download
        self.upload = upload or self.upload
        self.dl_bytes = dl_bytes or self.dl_bytes
        self.ul_bytes = ul_bytes or self.ul_bytes
        self.share_url = share_url or self.share_url
        self.data = data or self.data

        if not self.duration:
            self.duration = duration or (datetime.now() - self.start_time).total_seconds()

        self.save()

    @classmethod
    def create(cls, server, success, start_time, duration, server_id, latency, jitter, download, upload, dl_bytes,
               ul_bytes, share_url, is_average=False, data=None):
        obj = cls(
            server=server,
            success=success,
            start_time=start_time,
            duration=duration,
            server_id=server_id,
            latency=latency,
            jitter=jitter,
            download=download,
            upload=upload,
            dl_bytes=dl_bytes,
            ul_bytes=ul_bytes,
            share_url=share_url,
            data=data,

            test_date=datetime.date(start_time),
            entry_type='SPEED',
            is_average=is_average
        )
        obj.save()
        return obj


class PingTest(BaseTestModel):
    ping = models.FloatField('Average ping', default=0.0)
    stats = models.CharField('Ping Values', max_length=100)
    packet_loss = models.FloatField("Packet loss", null=True)

    def __str__(self):
        return f'PingTest(server={self.server}, ping={self.ping}, time={self.start_time}, success={self.success})'

    @classmethod
    def create(cls, server, ping, packet_loss, stats, success, start_time, duration, data=None):
        obj = cls(
            server=server,
            ping=ping,
            packet_loss=packet_loss,
            stats=stats,
            success=success,
            start_time=start_time,
            duration=duration,
            data=data,

            test_date=datetime.date(start_time),
            entry_type='PING'
        )
        obj.save()
        return obj


class DnsTest(BaseTestModel):
    ip = models.CharField('IP', null=True, max_length=15)

    def __str__(self):
        return f'DNS(server={self.server}, ip={self.ip}, time={self.start_time}, success={self.success})'

    @classmethod
    def create(cls, host, ip, success, start_time, duration, data=None):
        obj = cls(
            server=host,
            ip=ip,
            success=success,
            start_time=start_time,
            duration=duration,
            data=data,

            test_date=datetime.date(start_time),
            entry_type='DNS'
        )
        obj.save()
        return obj

