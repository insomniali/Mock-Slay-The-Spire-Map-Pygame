import math
import pygame

from helper import ImageLoader
from .dot import Dot


class Edge:

    def __init__(self, gamemap, srcx, srcy, dstx, dsty):
        self.gamemap = gamemap
        self.srcx = srcx
        self.srcy = srcy
        self.dstx = dstx
        self.dsty = dsty
        self.dots = []
        self.initialize_dots()

    def initialize_dots(self):
        if self.srcy < 0:
            return

        srcnode = self.gamemap.get_node(self.srcx, self.srcy)
        dstnode = self.gamemap.get_node(self.dstx, self.dsty)
        y_offset = 64 if self.dsty != 15 else 0
        srcpos = pygame.math.Vector2(srcnode.posx + 32, srcnode.posy + 20)
        dstpos = pygame.math.Vector2(dstnode.posx + 32, dstnode.posy + y_offset - 20)
        angle = pygame.math.Vector2().angle_to(dstpos - srcpos) if srcpos.x != dstpos.x else 0
        dis = srcpos.distance_to(dstpos)
        times = math.ceil(dis) // 16
        for i in range(times):
            lerp_pos = pygame.Vector2.lerp(srcpos, dstpos, i / times)
            pos = (lerp_pos.x - 8, lerp_pos.y - 16)
            surf = ImageLoader.DOT.copy()
            surf = pygame.transform.rotate(surf, angle)
            self.dots.append(Dot(self.gamemap, *pos, surf))

    def update(self, dt):
        for dot in self.dots:
            dot.update(dt)
