from django.db import models


# Create your models here.
class CdPlane(models.Model):
    """
    成都
    """
    # hr_img = models.CharField(max_length=1024)
    # job_detail_re = models.CharField(max_length=2048)
    # job_detail_location = models.CharField(max_length=1024)
    # key_id = models.IntegerField(default=0)
    flightno = models.CharField(max_length=64)
    flightcompany = models.CharField(max_length=32)
    flightdepcode = models.CharField(max_length=32)
    flightarrcode = models.CharField(max_length=32)
    flightdeptimeplandate = models.DateTimeField(null=True, blank=True)
    flightarrtimeplandate = models.DateTimeField(null=True, blank=True)
    flightdeptimedate = models.DateTimeField(null=True, blank=True)
    flightarrtimedate = models.DateTimeField(null=True, blank=True)
    checkintable = models.CharField(max_length=32)
    boardgate = models.CharField(max_length=32)
    baggageid = models.CharField(max_length=32)
    flightstate = models.CharField(max_length=32)
    flighthterminal = models.CharField(max_length=32)
    flightterminal = models.CharField(max_length=32)
    flightdepairport = models.CharField(max_length=32)
    flightarrairport = models.CharField(max_length=32)
    ontimerate = models.CharField(max_length=32)
    generic = models.CharField(max_length=64)
    flightyear = models.CharField(max_length=32)
    depWeather = models.CharField(max_length=64)
    arrweather = models.CharField(max_length=64)
    distance = models.CharField(max_length=64)
    depweathertemper = models.CharField(max_length=32)
    arrweathertemper = models.CharField(max_length=32)
    flightdep = models.CharField(max_length=32)
    flightarr = models.CharField(max_length=32)

    def to_dict(self):
        return {
            # 'flightdep': self.flightdep,
            'flightarr': self.flightarr,
        }

    def to_all_dict(self):
        return {
            'flightno': self.flightno,
            'flightcompany': self.flightcompany,
            'flightdepcode': self.flightdepcode,
            'flightarrcode': self.flightarrcode,
            'flightdeptimeplandate': self.flightdeptimeplandate,
            'flightarrtimeplandate': self.flightarrtimeplandate,
            'flightdeptimedate': self.flightdeptimedate,
            'flightarrtimedate': self.flightarrtimedate,
            'checkintable': self.checkintable,
            'boardgate': self.boardgate,
            'baggageid': self.baggageid,
            'flightstate': self.flightstate,
            'flighthterminal': self.flighthterminal,
            'flightterminal': self.flightterminal,
            'flightdepairport': self.flightdepairport,
            'flightarrairport': self.flightarrairport,
            'ontimerate': self.ontimerate,
            'generic': self.generic,
            'flightyear': self.flightyear,
            'depWeather': self.depWeather,
            'arrweather': self.arrweather,
            'distance': self.distance,
            'depweathertemper': self.depweathertemper,
            'arrweathertemper': self.arrweathertemper,
            'flightdep': self.flightdep,
            'flightarr': self.flightarr
        }

    class Meta:
        db_table = 'cd_plane'
