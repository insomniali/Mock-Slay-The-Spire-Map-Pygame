import logging
import pygame
import sys

from dungeon import Dungeon
from helper import EventCenter, ImageLoader


_LOGGER = logging.getLogger("app")


class Application:

    def __init__(self):
        self.clock = None
        self.dungeon = None

    def launch(self):
        pygame.init()

        # 初始化分辨率
        width, height = 1920, 1080
        pygame.display.set_mode((width, height))
        pygame.display.set_caption("Demo")

        # 初始化时钟
        self.clock = pygame.time.Clock()

        # 加载图片
        ImageLoader.load_image()

        # 初始化地图
        self.dungeon = Dungeon()
        self.dungeon.generate_map()

        self.run()

    def run(self):
        try:
            loop = True
            while loop:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        loop = False
                    EventCenter.process_event(event)
                dt = self.clock.tick(60) / 1000
                self.dungeon.update(dt)
                pygame.display.update()
                pygame.display.get_surface().fill("black")
        except Exception as e:
            # import traceback
            # traceback.print_exc()
            _LOGGER.debug("err %s", e)
        finally:
            self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()


if "APP" not in globals():
    APP = Application()
