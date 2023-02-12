import logging
import random

from room import ALL_ROOM, ERoomType

_LOGGER = logging.getLogger("roomassigner")


class RoomTypeAssigner:

    @classmethod
    def assign_row_as_roomtype(cls, row_nodes, roomtype):
        for node in row_nodes:
            if node.has_room():
                continue
            room = ALL_ROOM[roomtype]()
            node.set_room(room)

    @classmethod
    def distribute_rooms_across_map(cls, map_nodes, roomtype_info):
        count = get_connected_non_assign_node_count(map_nodes)
        total_room = sum(roomtype_info)
        if total_room < count:
            roomtype_info[ERoomType.MONSTER] = count - total_room
        else:
            _LOGGER.debug("distribute_rooms error count less than roomtypes")
        assign_rooms_to_nodes(map_nodes, roomtype_info)

    @classmethod
    def assign_boss_room(self, node):
        room = ALL_ROOM[ERoomType.BOSS]()
        node.set_room(room)


def get_connected_non_assign_node_count(map_nodes):
    count = 0
    for raw_nodes in map_nodes:
        for node in raw_nodes:
            if not node.has_edge():
                continue
            if node.has_room():
                continue
            count += 1
    return count


def assign_rooms_to_nodes(map_nodes, roomtype_info):
    for raw_nodes in map_nodes:
        for node in raw_nodes:
            if not node.has_edge():
                continue
            if node.has_room():
                continue
            room_to_be_set = get_next_roomtype_according_to_rules(map_nodes, node, roomtype_info)
            if not room_to_be_set:
                continue
            roomtype_info[room_to_be_set] -= 1
            room = ALL_ROOM[room_to_be_set]()
            node.set_room(room)


def get_next_roomtype_according_to_rules(map_nodes, node, roomtype_info):
    room_t = None
    parents = node.get_parents()
    siblings = get_siblings(map_nodes, parents, node)
    roomtype_list = list(roomtype_info)
    random.shuffle(roomtype_list)
    for roomtype in roomtype_list:
        if not roomtype_info[roomtype]:
            continue
        if rule_assignable_to_row(node, roomtype):
            if not rule_parent_matches(parents, roomtype) and not rule_sibling_matches(siblings, roomtype):
                room_t = roomtype
                break
    return room_t if room_t else ERoomType.MONSTER


def get_siblings(map_nodes, parents, node):
    siblings = []
    for parent in parents:
        for edge in parent.get_edges():
            sibling_node = map_nodes[edge.dsty][edge.dstx]
            if sibling_node == node:
                continue
            siblings.append(sibling_node)
    return siblings


def rule_assignable_to_row(node, roomtype):
    ban_roomtype = (ERoomType.REST, ERoomType.ELITE, )
    ban_roomtype2 = (ERoomType.REST, )
    # 四层及以下不出现休息房与精英房
    if node.y <= 4 and roomtype in ban_roomtype:
        return False
    # 十三层及以上不出现休息房
    if node.y >= 13 and roomtype in ban_roomtype2:
        return False
    return True


def rule_parent_matches(parents, roomtype):
    """ 父母结点匹配规则
    """
    applicable_roomtype = (ERoomType.REST, ERoomType.TREASURE, ERoomType.SHOP, ERoomType.ELITE, )
    for parent in parents:
        if roomtype in applicable_roomtype and \
                roomtype == parent.get_room().roomtype:
            return True
    return False


def rule_sibling_matches(siblings, roomtype):
    """ 兄弟结点匹配规则
    """
    applicable_roomtype = (ERoomType.REST, ERoomType.MONSTER, ERoomType.EVENT, ERoomType.SHOP, ERoomType.ELITE, )
    for sibling in siblings:
        if sibling.get_room() and \
                roomtype in applicable_roomtype and \
                roomtype == sibling.get_room().roomtype:
            return True
    return False
