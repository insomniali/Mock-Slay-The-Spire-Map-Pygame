import pygame
import random
from room import ERoomType


class Node:

    def __init__(self, gamemap, x, y):
        self.gamemap = gamemap
        self.x = x
        self.y = y

        y_offset = random.randrange(15, 20) if self.x % 2 else random.randrange(-20, -15)
        self.posx = 485 + self.x * 135
        self.posy = 805 - self.y * 170 + y_offset

        self.room = None
        self.edges = []
        self.parents = []

    def has_edge(self):
        return True if self.edges else False

    def add_edge(self, edge):
        if edge in self.edges:
            return
        self.edges.append(edge)

    def del_edge(self, edge):
        if edge not in self.edges:
            return
        self.edges.remove(edge)

    def sort_edge(self):
        self.edges.sort(key=lambda e: (e.dstx, e.dsty))

    def get_edges(self):
        return self.edges

    def get_max_edge(self):
        self.sort_edge()
        if not self.has_edge():
            return
        return self.edges[-1]

    def get_min_edge(self):
        self.sort_edge()
        if not self.has_edge():
            return
        return self.edges[0]

    def add_parent(self, node):
        if node in self.parents:
            return
        self.parents.append(node)

    def get_parents(self):
        return self.parents

    def has_room(self):
        return False if not self.room else True

    def set_room(self, room):
        self.room = room

    def get_room(self):
        return self.room

    def __repr__(self) -> str:
        return f"node_({self.x, self.y})"

    def update(self, dt):
        self.render()

        for edge in self.edges:
            edge.update(dt)

    def render(self):
        if not self.room:
            return

        if self.room.roomtype == ERoomType.BOSS:
            self.render_top()
            return

        surf = self.room.images()
        screen = pygame.display.get_surface()
        screen.blit(surf, (self.posx, self.posy + self.gamemap.wheel_offset))

    def render_top(self):
        if not self.room:
            return

        surf = self.room.images()
        x = 704
        y = -2050 + self.gamemap.wheel_offset
        screen = pygame.display.get_surface()
        screen.blit(surf, (x, y))
