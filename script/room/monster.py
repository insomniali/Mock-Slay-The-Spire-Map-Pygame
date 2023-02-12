from helper import ImageLoader

from .base import BaseRoom
from .const import ERoomType


class MonsterRoom(BaseRoom):
    roomtype = ERoomType.MONSTER

    def images(self):
        return ImageLoader.MONSTER
