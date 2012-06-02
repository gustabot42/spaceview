from django.conf import settings
from appconf import AppConf


class SpaceviewConf(AppConf):
    
    SPACES = []    # List of SpaceView based views
