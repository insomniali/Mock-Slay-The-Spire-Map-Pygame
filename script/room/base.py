from .const import ERoomType


class BaseRoom:
    roomtype = ERoomType.BASE

    def text(self):
        return "基本"
