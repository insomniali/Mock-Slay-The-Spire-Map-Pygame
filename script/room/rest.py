from helper import ImageLoader

from .base import BaseRoom
from .const import ERoomType


class RestRoom(BaseRoom):
    roomtype = ERoomType.REST

    def images(self):
        return ImageLoader.REST
