from .boss import BossRoom
from .const import ERoomType
from .elite import EliteRoom
from .event import EventRoom
from .monster import MonsterRoom
from .rest import RestRoom
from .shop import ShopRoom
from .treasure import TreasureRoom


ALL_ROOM = {
    BossRoom.roomtype: BossRoom,
    EliteRoom.roomtype: EliteRoom,
    EventRoom.roomtype: EventRoom,
    MonsterRoom.roomtype: MonsterRoom,
    RestRoom.roomtype: RestRoom,
    ShopRoom.roomtype: ShopRoom,
    TreasureRoom.roomtype: TreasureRoom,
}


__all__ = [
    "ERoomType",
    "ALL_ROOM",
]
