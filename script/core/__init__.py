from .logger import setup
from .application import APP


def launch():
    setup()
    APP.launch()
