from helper import ImageLoader

from .base import BaseRoom
from .const import ERoomType


class TreasureRoom(BaseRoom):
    roomtype = ERoomType.TREASURE

    def images(self):
        return ImageLoader.CHEST
