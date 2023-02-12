import pygame
import random

from helper import EventCenter, ImageLoader
from room import ERoomType
from .edge import Edge
from .node import Node
from .roomassigner import RoomTypeAssigner


class Map:

    def __init__(self, height, width, density):
        self.height = height
        self.width = width
        self.density = density
        self.nodes = []
        self.boss_node = None
        self.wheel_offset = 0
        self.wheel_speed = 0
        EventCenter.subscribe(pygame.MOUSEWHEEL, self.on_mousewheel, "map_on_mousewheel")

    def on_mousewheel(self, event):
        self.wheel_speed = event.y

    def generator(self, dungeon):
        self.create_nodes()
        self.create_paths()
        self.filter_redundant_edge_from_row()

        roomtype_info = self.generator_roomtypes(dungeon)
        RoomTypeAssigner.assign_row_as_roomtype(self.nodes[-1], ERoomType.REST)
        RoomTypeAssigner.assign_row_as_roomtype(self.nodes[0], ERoomType.MONSTER)
        RoomTypeAssigner.assign_row_as_roomtype(self.nodes[8], ERoomType.TREASURE)
        RoomTypeAssigner.distribute_rooms_across_map(self.nodes, roomtype_info)

    def create_nodes(self):
        for y in range(self.height):
            raw_nodes = [Node(self, x, y) for x in range(self.width)]
            self.nodes.append(raw_nodes)

    def create_paths(self):
        """ 根据路径密度创建多条路径
        """
        self.boss_node = Node(self, self.width // 2, self.height)
        RoomTypeAssigner.assign_boss_room(self.boss_node)

        first_row = 0
        row_size = len(self.nodes[first_row]) - 1

        first_start_node = -1

        for i in range(self.density):
            start_node = random.randrange(0, row_size)

            if i == 0:
                first_start_node = start_node

            while (start_node == first_start_node and i == 1):
                start_node = random.randrange(0, row_size)

            self._create_path(Edge(self, start_node, -1, start_node, 0))

    def _create_path(self, edge):
        """ 创建单条路径
        """
        current_node = self.get_node(edge.dstx, edge.dsty)
        if edge.dsty + 1 >= len(self.nodes):
            new_edge = Edge(self, edge.dstx, edge.dsty, self.width // 2, edge.dsty + 1)
            current_node.add_edge(new_edge)
            current_node.sort_edge()
            return

        row_width = len(self.nodes[edge.dsty])
        row_end_node = row_width - 1

        # 左右随机偏移一格位置取候选结点
        left_offset = 0 if edge.dstx == 0 else -1
        right_offset = 0 if edge.dstx == row_end_node else 1
        new_edge_x = edge.dstx + random.randint(left_offset, right_offset)
        new_edge_y = edge.dsty + 1

        # 根据祖先节点位置调整偏移
        candidate_node = self.get_node(new_edge_x, new_edge_y)
        min_ancestor_gap = 3
        max_ancestor_gap = 5
        parents = candidate_node.get_parents()
        for parent in parents:
            if parent == current_node:
                continue
            ancestor = self.get_common_ancestor(parent, current_node, max_ancestor_gap)
            if not ancestor:
                continue
            ancestor_gap = new_edge_y - ancestor.y
            if ancestor_gap < min_ancestor_gap:
                if candidate_node.x > current_node.x:
                    new_edge_x = max(edge.dstx + random.randint(-1, 0), 0)
                elif candidate_node.x == current_node.x:
                    new_edge_x = min(edge.dstx + random.randint(-1, 0), row_end_node)
                    new_edge_x = max(new_edge_x, 0)
                candidate_node = self.get_node(new_edge_x, new_edge_y)
            if ancestor_gap >= max_ancestor_gap:
                pass

        # 根据同层节点位置调整偏移
        if edge.dstx != 0:
            left_node = self.nodes[edge.dsty][edge.dstx - 1]
            if left_node.has_edge():
                right_edge_of_left_node = left_node.get_max_edge()
                if right_edge_of_left_node.dstx > new_edge_x:
                    new_edge_x = right_edge_of_left_node.dstx
        if edge.dstx < row_end_node:
            right_node = self.nodes[edge.dsty][edge.dstx + 1]
            if right_node.has_edge():
                left_edge_of_right_node = right_node.get_min_edge()
                if left_edge_of_right_node.dstx < new_edge_x:
                    new_edge_x = left_edge_of_right_node.dstx

        candidate_node = self.get_node(new_edge_x, new_edge_y)
        new_edge = Edge(self, edge.dstx, edge.dsty, new_edge_x, new_edge_y)
        current_node.add_edge(new_edge)
        candidate_node.add_parent(current_node)
        return self._create_path(new_edge)

    def get_node(self, x, y):
        if y == self.height:
            return self.boss_node
        return self.nodes[y][x]

    def get_common_ancestor(self, parent, current_node, max_depth):
        """ 获取结点共同祖先节点
        """
        assert parent.y == current_node.y, "get_common_ancestor y error"
        assert parent != current_node, "get_common_ancestor node error"

        l_node = parent if parent.x < current_node.x else current_node
        r_node = parent if l_node == current_node else current_node
        current_y = parent.y
        while (current_y >= 0 and current_y >= parent.y - max_depth):
            if not l_node.get_parents() or not r_node.get_parents():
                return
            l_node = self.get_node_with_maxx(l_node.get_parents())
            r_node = self.get_node_with_minx(r_node.get_parents())
            if l_node == r_node:
                return l_node
            current_y -= 1

    def get_node_with_maxx(self, nodes):
        assert nodes, "get_node_with_maxx, nodes error"
        nodes.sort(key=lambda n: n.x)
        return nodes[-1]

    def get_node_with_minx(self, nodes):
        assert nodes, "get_node_with_minx, nodes error"
        nodes.sort(key=lambda n: n.x)
        return nodes[0]

    def filter_redundant_edge_from_row(self):
        """ 按行清理节点冗余边
        """
        exist_edges = []
        delete_edges = []
        for node in self.nodes[0]:
            for edge in node.get_edges():
                for pre_edge in exist_edges:
                    if edge.dstx == pre_edge.dstx and edge.dsty == pre_edge.dsty:
                        delete_edges.append(edge)
                exist_edges.append(edge)
            for edge in delete_edges:
                node.del_edge(edge)

    def generator_roomtypes(self, dungeon):
        valid_count = self.get_avaliable_nodes_count()
        roomtype_info = {
            ERoomType.SHOP: round(valid_count * dungeon.shoproom_chance),
            ERoomType.REST: round(valid_count * dungeon.restroom_chance),
            ERoomType.TREASURE: round(valid_count * dungeon.treasureroom_chance),
            ERoomType.ELITE: round(valid_count * dungeon.eliteroom_chance),
            ERoomType.EVENT: round(valid_count * dungeon.eventroom_chance)
        }
        return roomtype_info

    def get_avaliable_nodes_count(self):
        count = 0
        raw_size = len(self.nodes)
        for raw_nodes in self.nodes:
            for node in raw_nodes:
                if not node.has_edge() or node.y == raw_size - 2:
                    continue
                count += 1
        return count

    def update(self, dt):
        self.wheel_offset += self.wheel_speed * dt * 2000
        self.wheel_speed = 0
        self.render()
        for raw_nodes in self.nodes:
            for node in raw_nodes:
                if not node.has_edge():
                    continue
                node.update(dt)
        self.boss_node.update(dt)

    def render(self):
        screen = pygame.display.get_surface()
        screen.blits(
            [
                (ImageLoader.MAPTOP, (0, 0 + self.wheel_offset - 1080 * 2), ),
                (ImageLoader.MAPMID, (0, 0 + self.wheel_offset - 1080), ),
                (ImageLoader.MAPBOT, (0, 0 + self.wheel_offset), ),
            ]
        )
