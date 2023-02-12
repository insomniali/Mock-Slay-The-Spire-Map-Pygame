import pygame


class ImageLoader:

    @classmethod
    def load_image(cls):

        cls.MAPTOP = pygame.image.load(r"../images/map/mapTop.png").convert_alpha()
        cls.MAPMID = pygame.image.load(r"../images/map/mapMid.png").convert_alpha()
        cls.MAPBOT = pygame.image.load(r"../images/map/mapBot.png").convert_alpha()

        cls.DOT = pygame.image.load(r"../images/map/dot.png").convert_alpha()
        cls.CHEST = pygame.transform.scale(pygame.image.load(r"../images/map/chest.png").convert_alpha(), (64, 64))
        cls.ELITE = pygame.transform.scale(pygame.image.load(r"../images/map/elite.png").convert_alpha(), (64, 64))
        cls.EVENT = pygame.transform.scale(pygame.image.load(r"../images/map/event.png").convert_alpha(), (64, 64))
        cls.MONSTER = pygame.transform.scale(pygame.image.load(r"../images/map/monster.png").convert_alpha(), (64, 64))
        cls.REST = pygame.transform.scale(pygame.image.load(r"../images/map/rest.png").convert_alpha(), (64, 64))
        cls.SHOP = pygame.transform.scale(pygame.image.load(r"../images/map/shop.png").convert_alpha(), (64, 64))
        cls.BOSS = pygame.image.load(r"../images/map/slime.png").convert_alpha()
