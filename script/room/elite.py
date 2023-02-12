from helper import ImageLoader

from .const import ERoomType
from .monster import MonsterRoom


class EliteRoom(MonsterRoom):
    roomtype = ERoomType.ELITE

    def images(self):
        return ImageLoader.ELITE
