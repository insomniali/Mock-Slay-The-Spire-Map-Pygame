from helper import ImageLoader
from .const import ERoomType
from .monster import MonsterRoom


class BossRoom(MonsterRoom):
    roomtype = ERoomType.BOSS

    def images(self):
        return ImageLoader.BOSS
