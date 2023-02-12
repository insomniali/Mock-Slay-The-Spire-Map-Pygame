import pygame


class Dot:

    def __init__(self, gamemap, x, y, surf):
        self.gamemap = gamemap
        self.posx = x
        self.posy = y
        self.surf = surf

    def update(self, dt):
        self.render()

    def render(self):
        screen = pygame.display.get_surface()
        screen.blit(self.surf, (self.posx, self.posy + self.gamemap.wheel_offset))
        # debug
        # pygame.draw.rect(screen, "red", (self.posx, self.posy + dungeon.wheel_offset, 16, 16), 5)
