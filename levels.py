from settings import *
import pytmx as pt

class Level:
    def __init__(self, level=None):
        self.back1 = load_image('images/free-swamp-game-tileset-pixel-art/2 Background/Layers/1.png', SCREEN_SIZE)
        self.back2 = load_image('images/free-swamp-game-tileset-pixel-art/2 Background/Layers/2.png', SCREEN_SIZE)
        self.back3 = load_image('images/free-swamp-game-tileset-pixel-art/2 Background/Layers/3.png', SCREEN_SIZE)
        self.back4 = load_image('images/free-swamp-game-tileset-pixel-art/2 Background/Layers/4.png', SCREEN_SIZE)
        self.back5 = load_image('images/free-swamp-game-tileset-pixel-art/2 Background/Layers/5.png', SCREEN_SIZE)
        if level:
            self.level = pt.util_pygame.load_pygame(level)
        else:
            self.level = level

    def draw(self, screen):
       screen.blit(self.back1,(0,0))
       screen.blit(self.back2, (0, 0))
       screen.blit(self.back3, (0, 0))
       screen.blit(self.back4, (0, 0))

       if self.level:
           for layer in self.level.layers:

                for x, y, gid in layer:
                    tile = self.level.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pg.transform.scale(tile, (50, 58))
                    if tile:
                        screen.blit(tile, (x * 50, y * 58))
       screen.blit(self.back5, (0, 0))

    def event(self, event):
        pass

    def update(self):
        pass

class Foreground:
    def __init__(self):
        self.image = load_image('images/free-swamp-game-tileset-pixel-art/2 Background/Layers/5.png', SCREEN_SIZE)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

class Level_2:
    def __init__(self, level=None):
        self.back1 = load_image('images/Winter.jpg', SCREEN_SIZE)

        if level:
            self.level = pt.util_pygame.load_pygame(level)
        else:
            self.level = level

    def draw(self, screen):
       screen.blit(self.back1,(0,0))

       if self.level:
           for layer in self.level.layers:

                for x, y, gid in layer:
                    tile = self.level.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pg.transform.scale(tile, (50, 58))
                    if tile:
                        screen.blit(tile, (x * 50, y * 58))


    def event(self, event):
        pass

    def update(self):
        pass

class Level_3:
    def __init__(self, level=None):
        self.back1 = load_image('images/Space_ship.gif', SCREEN_SIZE)

        if level:
            self.level = pt.util_pygame.load_pygame(level)
        else:
            self.level = level

    def draw(self, screen):
       screen.blit(self.back1,(0,0))

       if self.level:
           for layer in self.level.layers:

                for x, y, gid in layer:
                    tile = self.level.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pg.transform.scale(tile, (50, 58))
                    if tile:
                        screen.blit(tile, (x * 50, y * 58))


    def event(self, event):
        pass

    def update(self):
        pass

class Slide_show:
    def __init__(self):
        self.button_return = Button('Return', (SCREEN_SIZE[0] // 8.5, SCREEN_SIZE[1] // 1.1), MAIN_MENU_EVENT)
        self.images = [
            load_image('images/Screenshots/Level1.png', SCREEN_SIZE),
            load_image('images/Screenshots/Level2.png', SCREEN_SIZE),
            load_image('images/Screenshots/Level3.png', SCREEN_SIZE)
        ]
        self.index_image = 0
        self.timer = pg.time.get_ticks()
        self.text = "BigZver"
        self.text3 = "Vee_show"
        self.font = pg.font.Font('Pixsel_font.ttf', 50)
        self.image = self.font.render(self.text, True, (0, 0, 0))
        self.image3 = self.font.render(self.text3, True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)
        self.rect3 = self.image3.get_rect()
        self.rect3.midtop = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)
        self.text2 = "THANKS FOR PLAYING! :)"
        self.font2 = pg.font.Font('Pixsel_font.ttf', 60)
        self.image2 = self.font2.render(self.text2, True, 'green')
        self.rect2 = self.image2.get_rect()
        self.rect2.center = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)

    def update(self):
        if pg.time.get_ticks() - self.timer > 3000:
            self.index_image += 1
            if self.index_image == 3:
                self.index_image = 0
            self.timer = pg.time.get_ticks()


    def draw(self, screen):
        screen.blit(self.images[self.index_image], (0, 0))
        self.button_return.draw(screen)
        if self.index_image == 0 or self.index_image == 1:
            screen.blit(self.image, self.rect)
            screen.blit(self.image3, self.rect3)
        else:
            screen.blit(self.image2, self.rect2)


    def event(self, event):
        self.button_return.event(event)

class Settings_LOL:
    def __init__(self):
        self.button_return = Button('Return', (SCREEN_SIZE[0] // 8.5, SCREEN_SIZE[1] // 1.1), MAIN_MENU_EVENT)
        self.text = 'What do you want to do here? Lol'
        self.font = pg.font.Font('Pixsel_font.ttf', 50)
        self.image = self.font.render(self.text, True, 'white')
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.image, self.rect)
        self.button_return.draw(screen)


    def event(self, event):
        self.button_return.event(event)

    def update(self):
        pass