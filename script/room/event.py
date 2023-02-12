from helper import ImageLoader

from .base import BaseRoom
from .const import ERoomType


class EventRoom(BaseRoom):
    roomtype = ERoomType.EVENT

    def images(self):
        return ImageLoader.EVENT
