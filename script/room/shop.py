from helper import ImageLoader

from .base import BaseRoom
from .const import ERoomType


class ShopRoom(BaseRoom):
    roomtype = ERoomType.SHOP

    def images(self):
        return ImageLoader.SHOP
